import time
from random import random, randrange

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from manager_app import ManagerApp

class Metrika:
    def createMetrika(self):
        ManagerApp.get_logger().info("Create metrika")
        driver = ManagerApp().get_driver()
        driver.execute_script('''window.open("https://metrika.yandex.ru","_blank");''')
        driver.switch_to.window(driver.window_handles[1])
        #driver.get("https://metrika.yandex.ru")

        ManagerApp.get_logger().info("Click button \"Add counter\"")
        driver.find_element_by_css_selector("div.counters-list__head > a").click()
        url_page = "https://"+ManagerApp().get_json_data()["header"]["title_page"]+".turbo.site/book"

        ManagerApp.get_logger().info("Set url-page="+url_page)
        driver.find_element_by_css_selector("input[placeholder='Домен или полный путь сайта']").send_keys(url_page)


        name_counter = ManagerApp().get_json_data()["header"]["title_page"]+" "+time.strftime("%d.%m.%Y")+" "+str(randrange(999))
        ManagerApp.get_logger().info("Set name-counter=" + name_counter)
        driver.find_element_by_xpath("//span[@class='input input_theme_normal input_size_s form-field form-field_type_input i-bem input_js_inited form-field_js_inited']//input[@class='input__control']")\
            .send_keys(name_counter)

        gmt = "(GMT+03:00) Москва, Санкт-Петербург"
        ManagerApp.get_logger().info("Set "+gmt)
        time_gmt = driver.find_element_by_xpath("//span[@class='input input_size_s input_search_yes input_theme_normal i-bem input_js_inited']//input[@class='input__control']")
        driver.execute_script("arguments[0].setAttribute('value',arguments[1])", time_gmt, gmt)


        driver.find_element_by_css_selector("#webvisor > div.counter-edit__tumbler-container-right > div > div").click()
        driver.find_element_by_css_selector("span[class*='popup i-bem checkbox_js_inited form-field_js_inited'] span[class='checkbox__box']").click()
        ManagerApp.get_logger().info("Click button save")
        driver.execute_script("arguments[0].click();",driver.find_element_by_xpath("//button//*[text()='Создать счетчик']"))

        #driver.find_element_by_css_selector("label[class*='radio tabs__tab']").click()
        driver.find_element_by_css_selector(".counter-edit__onboarding-content-wrapper")
        counter_id = driver.current_url.split("onboarding/", 1)[1].replace("?", "").strip()
        ManagerApp.get_logger().info("counter_id="+counter_id)
        return counter_id
    def create_goals(self):
        ManagerApp.get_logger().info("Create goals")
        driver = ManagerApp().get_driver()
        self.go_to_configure_goals(driver)
        self.create_goal_for_content(driver, "Зашли в ТС", "https://" + ManagerApp().get_json_data()["header"]["title_page"] + ".turbo.site/book")
        self.create_goal_for_content(driver, "Переход в текст", ManagerApp().get_json_data()["content"]["text_book"])
        self.create_goal_for_content(driver, "Переход на главную АТ", ManagerApp().get_json_data()["content"]["text_book_main"])
        self.create_goal_for_content(driver, "Переход на аудио", ManagerApp().get_json_data()["content"]["audio_book"])

        self.create_goal_for_social_media(driver, "Переход в ВК","ВКонтакте")
        self.create_goal_for_social_media(driver, "Переход в ФБ", "Facebook")
        self.create_goal_for_social_media(driver, "Переход в ОК", "Одноклассники")
        self.create_goal_for_social_media(driver, "Переход в ИНСТ", "instagram.com")
        self.create_goal_for_social_media(driver, "Переход в ПИН", "Pinterest")

    def go_to_configure_goals(self, driver):
        ManagerApp.get_logger().info("Click by url for configure goals")
        driver.find_element_by_css_selector("span[class*='go-to-goals-setup-link']").click()
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@class='button__text' and text()='Добавить цель']")))

    def create_goal_for_content(self, driver, name, url):
        ManagerApp.get_logger().info("Create goals: "+name)

        driver.find_element_by_css_selector("button[class*='button_theme_action counter-edit-table']").click()
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class*='action i-confirm-popup__button']")))

        driver.find_element_by_css_selector(
            "input[placeholder*='Например, клик по кнопке «Оставить заявку»']").send_keys(name)
        driver.find_element_by_css_selector("label[class*='both radio-button__radio_checked_yes']").click()
        driver.find_element_by_xpath(
            "//div[@class='counter-edit-table-row__condition']//input[@class='input__control']").send_keys(url)
        driver.find_element_by_css_selector(
            "div[class*='goal-value_indent'] input[class='input__control'][value='0']").send_keys("1")
        # driver.find_element_by_xpath("//div[@class='i-confirm-popup__buttons']//span[text()='Добавить цель']").click()
        driver.find_element_by_css_selector("button[class*='action i-confirm-popup__button']").click()


    def create_goal_for_social_media(self, driver, name, type_social_media):
        ManagerApp.get_logger().info("Create goals: "+name)
        driver.find_element_by_css_selector("button[class*='button_theme_action counter-edit-table']").click()
        WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "button[class*='action i-confirm-popup__button']")))
        driver.find_element_by_css_selector(
            "input[placeholder*='Например, клик по кнопке «Оставить заявку»']").send_keys(name)

        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_xpath("//span[@class='radio-button__text' and text()='Переход в соц. сеть']"))

        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_xpath("//span[@class='radiobox__text']//div[text()='Конкретная соц. сеть']"))

        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_xpath("//*[text()='Выберите соц. сеть']"))

        social_media_item = driver.find_element_by_xpath(
            "//*[@class='popup2 popup2_theme_normal popup2_target_anchor popup2_hiding_yes popup2_autoclosable_yes popup2_view_classic select2__popup i-bem popup2_js_inited popup2_direction_top-left popup2_visible_yes']//span[@class='menu__text' and contains(.,'%s')]" % type_social_media)
        driver.execute_script("arguments[0].click();",
                              social_media_item)
        driver.find_element_by_css_selector(
            "div[class*='pane_active_yes'] input[class='input__control'][value='0']")\
            .send_keys("1")
        # driver.find_element_by_xpath("//div[@class='i-confirm-popup__buttons']//span[text()='Добавить цель']").click()
        driver.find_element_by_css_selector("button[class*='action i-confirm-popup__button']").click()





