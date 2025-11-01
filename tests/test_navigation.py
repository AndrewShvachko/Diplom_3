import pytest
import allure
from data.data import Data
from pages.main_page import MainPage



@allure.feature('Навигация по разделам')
class TestNavigation:
    @allure.title('Переход в конструктор из ленты заказов')    
    def test_navigate_to_constructor_from_order_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_url(Data.BASE_URL)
        main_page.go_to_order_feed()
        main_page.go_to_constructor()
        assert main_page.is_element_visible(main_page.locators.CONSTRUCTOR_DROP_AREA),\
            "Конструктор не открылся после перехода из ленты заказов"
        

    @allure.title('Переход в ленту заказов из конструктора')
    def test_navigate_to_order_feed_from_constructor(self, driver):
        main_page = MainPage(driver) 
        main_page.open_url(Data.BASE_URL)
        main_page.go_to_order_feed()
        current_url = main_page.get_current_url()
        expected_url = f"{Data.BASE_URL}feed"
        assert current_url == expected_url,\
            f"Не перешли в ленту заказов. Ожидался URL: {expected_url}, получен: {current_url}"    
