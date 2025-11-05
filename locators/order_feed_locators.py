from selenium.webdriver.common.by import By



class OrderFeedLocators:

    TOTAL_ORDERS_COUNT = (By.XPATH, "//p[contains(@class, 'OrderFeed_number__2MbrQ') and preceding-sibling::p[contains(text(), 'Выполнено за все время')]]")
    TODAY_ORDERS_COUNT = (By.XPATH, "//p[contains(@class, 'OrderFeed_number__2MbrQ') and preceding-sibling::p[contains(text(), 'Выполнено за сегодня')]]")

    ORDER_CARDS = (By.XPATH, "//div[contains(@class, 'OrderHistory_listItem')]")

    ORDERS_IN_PROGRESS_SECTION = (By.XPATH, "//ul[preceding-sibling::p[contains(text(), 'В работе')]]")
    ORDERS_IN_PROGRESS = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")

   
