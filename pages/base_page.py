from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import allure



class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    @allure.step('Находим элемент {locator}')
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    @allure.step('Находим элементы {locator}')
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)
    
    @allure.step('Кликаем на элемент {locator}')
    def click_element(self, locator):
        element = self.find_element(locator)
        element.click()

    @allure.step('Проверяем видимость элемента {locator}')
    def is_element_visible(self, locator):
        try:
            return self.find_element(locator).is_displayed()
        except:
             return False


    @allure.step('Ждем видимость элемента {locator}')
    def wait_for_element_visible(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @allure.step('Открываем URL: {url}')
    def open_url(self, url):
        self.driver.get(url)


    @allure.step('Получаем текущий URL')
    def get_current_url(self):
        return self.driver.current_url

    @allure.step('Прокручиваем к элементу {locator}')
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)           


    @allure.step('Ожидаем увеличения значения')
    def wait_for_value_increase(self, get_value_func, initial_value, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: get_value_func() > initial_value
            )
            return True
        except TimeoutException:
            return False
        
    @allure.step('Ожидаем выполнения условия')
    def wait_for_condition(self, condition_func, timeout=30):
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: condition_func()
            )
            return True
        except TimeoutException:
            return False