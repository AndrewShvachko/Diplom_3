import pytest
import allure
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage


@allure.feature('Лента заказов')
class TestOrderFeed:
    
    @allure.title('Счетчик "Выполнено за всё время" увеличивается')
    def test_total_orders_counter_increases(self, driver, login_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)        
        main_page.go_to_order_feed()              
        initial_total = order_feed_page.get_total_orders_count()      
        main_page.go_to_constructor()     
        main_page.add_ingredient_to_constructor("bun")
        order_processed = main_page.place_order_and_wait()
        assert order_processed, "Заказ не был обработан"
        main_page.close_order_modal()
        main_page.go_to_order_feed()
        counter_increased = order_feed_page.wait_for_total_orders_increase(initial_total, 30)
        current_total = order_feed_page.get_total_orders_count()
        assert counter_increased, f"Счетчик не увеличился: было {initial_total}, сейчас {current_total}"
            
    @allure.title('Счетчик "Выполнено за сегодня" увеличивается')
    def test_today_orders_counter_increases(self, driver, login_user):
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        main_page.go_to_order_feed()
        initial_today = order_feed_page.get_today_orders_count()
        main_page.go_to_constructor()
        main_page.add_ingredient_to_constructor("bun")
        order_processed = main_page.place_order_and_wait()
        main_page.close_order_modal()
        main_page.go_to_order_feed()
        counter_increased = order_feed_page.wait_for_today_orders_increase(initial_today, 30)
        assert counter_increased,(
            f"Счетчик за сегодня не увеличился: было {initial_today}, "
            f"сейчас {order_feed_page.get_today_orders_count()}"
        )

    @allure.title('Заказ появляется в разделе "В работе"')
    def test_order_appears_in_progress_section(self, driver, login_user):
        email, password, name, access_token = login_user
        main_page = MainPage(driver)
        order_feed_page = OrderFeedPage(driver)
        main_page.go_to_constructor()
        main_page.add_ingredient_to_constructor("bun")
        order_processed = main_page.place_order_and_wait()
        assert order_processed, "Модалка заказа не открылась"
        order_number_appeared = main_page.wait_for_order_number(timeout=15)
        assert order_number_appeared, "Номер заказа не появился в модалке"
        number_changed = main_page.wait_for_real_order_number(timeout=60)
        assert number_changed, "Номер заказа не изменился на реальный"
        real_order_number = main_page.get_order_number_from_modal()
        main_page.close_order_modal()
        main_page.go_to_order_feed()
        assert order_feed_page.wait_for_order_in_progress(real_order_number, 15),\
            f"БАГ: Заказ {real_order_number} не появился в разделе 'В работе'. " \
            f"Фактически в разделе отображается '0{real_order_number}', но ожидается '{real_order_number}'. " \
            f"Проблема с форматом отображения номера заказа."

        
                