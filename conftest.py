import pytest
import requests
import allure
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from data.data import Data, DataHelper
from pages.main_page import MainPage 


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
    with allure.step("Создаем пользователя в системе через API"):
        response = requests.post(f"{Data.BASE_URL}api/auth/register", json=payload)
        assert response.status_code == 200, "Не удалось создать пользователя"
    access_token = response.json().get('accessToken')
    with allure.step("Возвращаем данные пользователя для теста"):
        yield email, password, name, access_token
    with allure.step("Удаляем пользователя после теста через API"):
        if access_token:
            headers = {'Authorization': f'Bearer {access_token}'}
            requests.delete(f"{Data.BASE_URL}api/auth/user", headers=headers)

@pytest.fixture
def login_user(driver, user_data):
    email, password, name, access_token = user_data
    with allure.step(f"Авторизуем пользователя {email} в UI"):
        main_page = MainPage(driver)
        main_page.open_url(Data.BASE_URL)
        main_page.click_element(main_page.locators.LOGIN_BUTTON_MAIN)
        main_page.find_element(main_page.locators.EMAIL_INPUT).send_keys(email)
        main_page.find_element(main_page.locators.PASSWORD_INPUT).send_keys(password)
        main_page.click_element(main_page.locators.LOGIN_BUTTON_AUTH)
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(main_page.locators.PLACE_ORDER_BUTTON)
        )
        is_authorized = main_page.is_element_visible(main_page.locators.PLACE_ORDER_BUTTON)
        assert is_authorized, "Не удалось авторизовать пользователя в UI"
        return email, password, name, access_token
                                