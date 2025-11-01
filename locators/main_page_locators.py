from selenium.webdriver.common.by import By



class MainPageLocators:

    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.LINK_TEXT, "Лента Заказов")


    INGREDIENT_SECTION_BUN = (By.XPATH, "//h2[text()='Булки']")
    INGREDIENT_SECTION_SAUCE = (By.XPATH, "//h2[text()='Соусы']")
    INGREDIENT_SECTION_MAIN = (By.XPATH, "//h2[text()='Начинки']")


    INGREDIENT_BUN = (By.XPATH, "//p[text()='Флюоресцентная булка R2-D3']")
    INGREDIENT_SAUCE = (By.XPATH, "//p[text()='Соус фирменный Space Sauce']")
    INGREDIENT_MAIN = (By.XPATH, "//p[text()='Мясо бессмертных моллюсков Protostomia']")

   
    MODAL_ROOT = (By.CLASS_NAME, "Modal_modal__P3_V5")  
    MODAL_OPENED_CLASS = "Modal_modal_opened__3ISw4"    
    INGREDIENT_MODAL_CLOSE = (By.CLASS_NAME, "Modal_modal__close_modified__3V5XS")
    

    INGREDIENT_DETAILS_NAME = (By.XPATH, "//p[@class='text text_type_main-medium mb-8']")
    
    
    INGREDIENT_COUNTER = (By.XPATH, ".//p[@class='counter_counter__num__3nue1']")
    CONSTRUCTOR_DROP_AREA = (By.CLASS_NAME, "BurgerConstructor_basket__list__l9dp_")
    

    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(@class, 'button_button__33qZ0') and contains(text(), 'Оформить заказ')]")
    ORDER_MODAL = (By.CLASS_NAME, "Modal_modal__P3_V5")
    ORDER_NUMBER = (By.XPATH, "//h2[contains(@class, 'Modal_modal__title_shadow__3ikwq')]")



    LOGIN_BUTTON_MAIN = (By.XPATH, "//button[text()='Войти в аккаунт']")
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Пароль']")
    LOGIN_BUTTON_AUTH = (By.XPATH, "//button[text()='Войти']")

   

    