import pytest
import requests
import allure
from selenium import webdriver
from data.data_helper import DataHelper
from pages.main_page import MainPage
from urls import Urls


@pytest.fixture(params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    driver.maximize_window() 
    yield driver
    driver.delete_all_cookies()
    driver.quit()      


@pytest.fixture
def user_data():
    with allure.step("Генерируем данные для нового пользователя"):
        email = DataHelper.generate_email()
        password = DataHelper.generate_password()
        name = DataHelper.generate_name()
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
    access_token = None
    try:
        with allure.step("Создаем пользователя в системе через API"):
            response = requests.post(f"{Urls.BASE_URL}api/auth/register", json=payload)
            if response.status_code != 200:
                pytest.fail(f"Не удалось создать пользователя: {response.status_code}")
            access_token = response.json().get('accessToken')
        yield email, password, name, access_token
    finally:
        with allure.step("Удаляем пользователя после теста через API"):
            if access_token:
                try:
                    headers = {'Authorization': f'Bearer {access_token}'}
                    requests.delete(f"{Urls.BASE_URL}api/auth/user", headers=headers)
                except Exception as e:
                    pass                   
    

@pytest.fixture
def login_user(driver, user_data):
    email, password, name, access_token = user_data
    with allure.step(f"Авторизуем пользователя {email} в UI"):
        main_page = MainPage(driver)
        main_page.open_url(Urls.BASE_URL)
        main_page.login(email, password)
        is_authorized = main_page.is_user_authorized()
        if not is_authorized:
            pytest.fail("Не удалось авторизовать пользователя в UI")
        return email, password, name, access_token    