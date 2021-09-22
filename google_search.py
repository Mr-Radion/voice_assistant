import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException


def init_driver():
    # Создает экземпляр драйвера;
    driver = webdriver.Chrome()
    # driver = WebDriver(executable_path='C:/Users/user/Desktop/projects/voice-assistant-test/chromedriver.exe')
    # WebDriverWait используется для того, чтобы дать драйверу подождать 5 секунд, перед следующим действием;
    # по умолчанию при get запросе от driver, событие onload игнорируется прежде чем сделать запрос, ожидая окончания
    # загрузки страницы, но при большом количестве ajax, нужно вручную вмешаться и задать время
    driver.wait = WebDriverWait(driver, 5)
    return driver


def lookup(driver, query):
    driver.get("http://www.google.com")  # Это открывает поисковую страницу Google
    try:
        # мы используем функцию WebDriverWait именно для того, чтобы дождаться появления этих элементов
        # элемент 1 это строка поиска box
        box = driver.wait.until(ec.presence_of_element_located(
            (By.NAME, "q")))
        box.send_keys(query)  # вводит текст в текстовое поле полученного элемента box
        # элемент 2 это кнопка поиска
        # очередность важна, элементы по очереди расположены
        button = driver.wait.until(ec.element_to_be_clickable(
            (By.NAME, "btnK")))  # атрибут name = btnK
        # box.clear()  # очистить содержимое текстового поля
        try:
            button.click()
        except ElementNotVisibleException:
            button = driver.wait.until(ec.visibility_of_element_located(
                (By.NAME, "btnG")))
            button.click()
        # box = driver.wait.until(ec.presence_of_element_located(
        #     (By.NAME, "q")))
        # box.clear()
    except TimeoutException:
        print("Box or Button not found in google.com")


driver_result = init_driver()
lookup(driver_result, "Selenium")
time.sleep(5)
# driver_result.close()  # закрывает вкладку браузера
driver_result.quit()  # закрывает браузер
