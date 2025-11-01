import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from .base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = MainPageLocators()

    @allure.step('Переходим в конструктор')
    def go_to_constructor(self):
        self.click_element(self.locators.CONSTRUCTOR_BUTTON)

    @allure.step('Переходим в ленту заказов')                               
    def go_to_order_feed(self):
        # оверлей модалки перекрывает ссылку "Лента заказов" даже после закрытия
        # поэтому решил использовать JS-клик                                              
        self.driver.execute_script("""
        var orderFeedLink = document.querySelector('a[href="/feed"]');
        if (orderFeedLink) orderFeedLink.click();
    """)

    @allure.step('Открываем детали ингредиента: {ingredient_type}')
    def open_ingredient_details(self, ingredient_type):
        if ingredient_type == "bun":
            self.click_element(self.locators.INGREDIENT_BUN)
        elif ingredient_type == "sauce":
            self.click_element(self.locators.INGREDIENT_SAUCE)
        elif ingredient_type == "main":
            self.click_element(self.locators.INGREDIENT_MAIN)

    @allure.step('Закрываем модальное окно ингредиента')
    def close_ingredient_modal(self):
        self.click_element(self.locators.INGREDIENT_MODAL_CLOSE)

       
    @allure.step('Проверяем открытие модального окна ингредиента')
    def is_ingredient_modal_opened(self):
        try:
            element = self.find_element(self.locators.MODAL_ROOT)
            return self.locators.MODAL_OPENED_CLASS in element.get_attribute('class')
        except:
            return False

    @allure.step('Проверяем закрытие модального окна ингредиента')
    def is_ingredient_modal_closed(self):
        try:
            element = self.find_element(self.locators.MODAL_ROOT)
            return self.locators.MODAL_OPENED_CLASS not in element.get_attribute('class')
        except:
            return True

    @allure.step('Получаем название ингредиента из модального окна')
    def get_ingredient_name_from_modal(self):
        return self.find_element(self.locators.INGREDIENT_DETAILS_NAME).text
  
   
    @allure.step('Получаем значение счетчика ингредиента: {ingredient_type}')
    def get_ingredient_counter_value(self, ingredient_type):
        try:
            if ingredient_type == "bun":
                ingredient_element = self.driver.find_element(*self.locators.INGREDIENT_BUN)
            elif ingredient_type == "sauce":
                ingredient_element = self.driver.find_element(*self.locators.INGREDIENT_SAUCE)
            elif ingredient_type == "main":
                ingredient_element = self.driver.find_element(*self.locators.INGREDIENT_MAIN)
            else:
                return "0"
            parent = ingredient_element.find_element(By.XPATH, "./..")
            counter_element = parent.find_element(By.XPATH, ".//p[@class='counter_counter__num__3nue1']")
            return counter_element.text
        except:
            return "0"            
                                     
        
    @allure.step('Добавляем ингредиент в конструктор: {ingredient_type}') 
    def add_ingredient_to_constructor(self, ingredient_type):
        if ingredient_type == "bun":
            source_locator = self.locators.INGREDIENT_BUN
        elif ingredient_type == "sauce":
            source_locator = self.locators.INGREDIENT_SAUCE
        elif ingredient_type == "main":
            source_locator = self.locators.INGREDIENT_MAIN
        target_locator = self.locators.CONSTRUCTOR_DROP_AREA
        self.drag_and_drop_improved(source_locator, target_locator)            

    @allure.step('Перетаскиваем элемент из {source_locator} в {target_locator}')
    def drag_and_drop_improved(self, source_locator, target_locator):
         self.find_element(source_locator)
         self.find_element(target_locator)
         element_from = self.driver.find_element(*source_locator)
         element_to = self.driver.find_element(*target_locator)
         self.driver.execute_script("""
        var source = arguments[0];
        var target = arguments[1];

        var evt = document.createEvent("DragEvent");
        evt.initMouseEvent("dragstart", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        source.dispatchEvent(evt);

        evt = document.createEvent("DragEvent");
        evt.initMouseEvent("dragenter", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        target.dispatchEvent(evt);

        evt = document.createEvent("DragEvent");
        evt.initMouseEvent("dragover", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        target.dispatchEvent(evt);

        evt = document.createEvent("DragEvent");
        evt.initMouseEvent("drop", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        target.dispatchEvent(evt);

        evt = document.createEvent("DragEvent");
        evt.initMouseEvent("dragend", true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0, null);
        source.dispatchEvent(evt);
    """, element_from, element_to)
        
   
    @allure.step('Оформляем заказ')
    def place_order(self):
        self.click_element(self.locators.PLACE_ORDER_BUTTON)

    @allure.step('Получаем номер заказа из модального окна')
    def get_order_number_from_modal(self):
        return self.find_element(self.locators.ORDER_NUMBER).text

    @allure.step('Проверяем открытие модального окна заказа')
    def is_order_modal_opened(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.ORDER_MODAL)
        )
            return True
        except:
            return False
        
        
    @allure.step('Ожидаем появление номера заказа в модалке')
    def wait_for_order_number(self, timeout=15):
        try:
            WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.locators.ORDER_NUMBER)
        )
            return True
        except:
            return False
        
    @allure.step('Ожидаем реальный номер заказа')
    def wait_for_real_order_number(self, timeout=30):
        initial_number = self.get_order_number_from_modal()
        return self.wait_for_condition(
            condition_func=lambda: self.get_order_number_from_modal() != initial_number,
            timeout=timeout
        )
            
    @allure.step('Оформляем заказ и ждем обработки')
    def place_order_and_wait(self):
        self.place_order()
        assert self.is_order_modal_opened(), "Модалка заказа не открылась"
        order_processed = self.wait_for_order_number(timeout=15)
        return order_processed

    @allure.step('Закрываем модальное окно заказа')         
    def close_order_modal(self):
        # так же проблемы с оверлеем поэтому использую JS-клик
        try:
            self.driver.execute_script("""
            var closeBtn = document.querySelector('.Modal_modal__close_modified__3V5XS');
            if (closeBtn) closeBtn.click();
        """)
            return True
        except:
            return False

   