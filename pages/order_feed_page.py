import allure
from .base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = OrderFeedLocators()

    @allure.step('Получаем общее количество выполненных заказов')
    def get_total_orders_count(self):
        try:
            count_text = self.find_element(self.locators.TOTAL_ORDERS_COUNT).text
            return int(count_text.replace(',', ''))
        except:
            return 0

    @allure.step('Получаем количество выполненных заказов за сегодня')
    def get_today_orders_count(self):
        try:
            count_text = self.find_element(self.locators.TODAY_ORDERS_COUNT).text
            return int(count_text.replace(',', ''))
        except:
            return 0


    @allure.step('Получаем номера заказов в работе')
    def get_orders_in_progress_numbers(self):
        try:
            section = self.find_element(self.locators.ORDERS_IN_PROGRESS_SECTION)
            orders = section.find_elements(*self.locators.ORDERS_IN_PROGRESS)
            return [order.text for order in orders if order.text.strip()]
        except:
            return []  
    
    
    @allure.step('Ожидаем увеличение счетчика заказов за сегодня')
    def wait_for_today_orders_increase(self, initial_count, timeout=30):
        return self.wait_for_value_increase(
            get_value_func=self.get_today_orders_count,
            initial_value=initial_count,
            timeout=timeout
        )

    @allure.step('Ожидаем увеличение общего счетчика заказов')
    def wait_for_total_orders_increase(self, initial_count, timeout=30):
        return self.wait_for_value_increase(
            get_value_func=self.get_total_orders_count,
            initial_value=initial_count,
            timeout=timeout
        )  

   
    @allure.step('Ожидаем появление заказа в разделе "В работе"')
    def wait_for_order_in_progress(self, order_number, timeout=30):
        return self.wait_for_condition(
            condition_func=lambda: order_number in self.get_orders_in_progress_numbers(),
            timeout=timeout
        )
        
            
            

            
