import pytest
import allure
from urls import Urls
from data.data import Data
from pages.main_page import MainPage

@allure.feature('Работа с ингредиентами')
class TestIngredients:
  

    
    @allure.title('Открытие и закрытие модального окна ингредиента')
    def test_ingredient_modal_open_and_close(self, driver):
        main_page = MainPage(driver)
        main_page.open_url(Urls.BASE_URL)       
        main_page.open_ingredient_details("bun")
        assert main_page.is_ingredient_modal_opened(), "Модальное окно ингредиента не открылось"    
        main_page.close_ingredient_modal()
        assert main_page.is_ingredient_modal_closed(), "Модальное окно ингредиента не закрылось"    


    
    @allure.title('Отображение деталей ингредиента в модальном окне')
    def test_ingredient_details_in_modal(self, driver):
        main_page = MainPage(driver)
        main_page.open_url(Urls.BASE_URL)
        main_page.open_ingredient_details("sauce")
        ingredient_name = main_page.get_ingredient_name_from_modal()
        assert Data.INGREDIENTS["sauce"] in ingredient_name,\
            f"Название ингредиента в модальном окне не соответствует ожидаемому"   


    @allure.title('Увеличение счетчика ингредиента при добавлении')
    def test_ingredient_counter_increases_when_added(self, driver):
        main_page = MainPage(driver)
        main_page.open_url(Urls.BASE_URL)
        counter_before = main_page.get_ingredient_counter_value("bun")
        main_page.add_ingredient_to_constructor("bun")
        counter_after = main_page.get_ingredient_counter_value("bun")            
        assert counter_before == "0", f"Начальный счетчик должен быть '0', а получили: '{counter_before}'"
        assert counter_after == "2", f"Счетчик после добавления должен быть '2', а получили: '{counter_after}'"
        
        
    
