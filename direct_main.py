from time import sleep

from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from manager_app import ManagerApp


class DirectMain:

    def open_yadirect(self):
        ManagerApp().get_driver().get("https://direct.yandex.ru/dna/grid/campaigns?filter=dim%20%3D%20%7C%D0%A1%D1%82%D0%B0%D1%82%D1%83%D1%81%20%3D%20%D0%92%D1%81%D0%B5%2C%20%D0%BA%D1%80%D0%BE%D0%BC%D0%B5%20%D0%B0%D1%80%D1%85%D0%B8%D0%B2%D0%BD%D1%8B%D1%85&ulogin=ak-adv-2")
    def click_new_section_button(self, driver):
        ManagerApp.get_logger().info("Click by \"Add section\" button")
        driver.find_element_by_xpath(
            "//*[@class='y-button y-button_theme_action y-button_size_l y-button_type_button designer-header__add-section']").click()
    def create_turbopage(self):
        ManagerApp.get_logger().info("Create turbo-page")
        driver = ManagerApp().get_driver()

        driver.find_element_by_xpath("//*[@title='Инструменты']").click()
        driver.find_element_by_xpath("//*[text()='Конструктор Турбо-страниц']").click()
        self.switch_to_frame(driver)
        driver.find_element_by_css_selector("span[class*='back icon_symbol']").click()
        sleep(1)
        driver.find_element_by_css_selector("span[class*='back icon_symbol']").click()

        ManagerApp.get_logger().info("Click by create button")
        driver.find_element_by_xpath("//button[contains(.,'Создать')]").click()
        driver.find_element_by_xpath("//span[text()='Турбо-сайт']").click()
        titlePageField = driver.find_element_by_xpath("//*[@class='templates__name']//*[@class='y-input__control']")

        ManagerApp.get_logger().info("Set name page")
        titlePageField.send_keys(Keys.CONTROL + "a")
        titlePageField.send_keys(Keys.DELETE)
        page_name = ManagerApp().get_json_data()["header"]["title_page"]
        titlePageField.send_keys(page_name)
        driver.find_element_by_xpath("//*[@class='y-button y-button_theme_action y-button_size_s y-button_type_button ']").click()

        self.create_header_section(driver)
        self.create_text_section(driver)
        self.add_photo(driver,ManagerApp().get_json_data()["graphic"]["path_photo1"],ManagerApp().get_json_data()["graphic"]["url_photo1"])
        self.add_full_description(driver)
        self.add_buttons(driver)
        self.add_photo(driver, ManagerApp().get_json_data()["graphic"]["path_photo2"],ManagerApp().get_json_data()["graphic"]["url_photo2"])
        self.add_buttons(driver)
        self.configure_footer(driver)

        self.open_settings(driver)

        ManagerApp.get_logger().info("Set site favicon")
        driver.find_element_by_css_selector("div[class='lpc-attach__dropzone'] > input[type=file]")\
            .send_keys(ManagerApp().get_json_data()["graphic"]["logo"])
        sleep(1)
        ManagerApp.get_logger().info("Click by Save")
        driver.find_element_by_css_selector(".y-button_theme_action.y-button_size_m.y-button_type_button").click()
        driver.find_element_by_css_selector(".lpc-attach__preview")
        self.configure_page(driver)
        self.save_and_publish_page(driver, page_name)

    def open_settings(self, driver):
        ManagerApp.get_logger().info("Click by settings page")
        driver.find_element_by_css_selector("span[class*='designer-gear icon_symbol']")
        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_css_selector("span[class*='designer-gear icon_symbol']"))

    def add_counter_to_page(self, driver, counter_id):
        self.open_settings(driver)
        self.click_by_page_settings(driver)
        self.click_by_yametrika(driver)

        type_counter_element = driver.find_element_by_css_selector("div[class*='select_theme_normal']")
        #driver.execute_script("arguments[0].click();", type_counter_element)
        type_counter_element.click()
        your_element = driver.find_element_by_css_selector("span[class='y-select__text']>span[title='Свой']")
        your_element.click()
        #driver.execute_script("arguments[0].click();", your_element)
        driver.find_element_by_css_selector("input[parentpath='yandexCounterId']").send_keys(counter_id)
        driver.find_element_by_css_selector("div.page-settings__footer > button").click()
        WebDriverWait(driver, 3).until(
                 EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.page-settings__footer > button")))
        self.open_settings(driver)
        self.click_by_site_settings(driver)
        self.click_by_yametrika(driver)

        if driver.find_elements_by_css_selector("div[class*='input_width_ lpc-text__input']").__sizeof__()>0:
            driver.execute_script("arguments[0].click();",driver.find_element_by_xpath("//div[@role='button' and contains(.,'Основные')]"))
        sleep(1)
        driver.execute_script("arguments[0].click();", driver.find_element_by_css_selector("button[class*='arrow_down y-select__button']"))
        driver.execute_script("arguments[0].click();",driver.find_element_by_css_selector("span[class='y-select__text']>span[title='Свой']"))

        driver.find_element_by_css_selector("input[name='metrikaCounter']").send_keys(counter_id)
        driver.find_element_by_css_selector("div.page-settings__footer > button").click()
        WebDriverWait(driver, 3).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, "div.page-settings__footer > button")))

    def click_by_save_settings(self, driver):
        driver.find_element_by_css_selector("div.page-settings__footer > button").click()
        driver.find_element_by_css_selector("div[class*='panel_visible designer-drawer__panel_animated")
        modal_form = driver.find_elements_by_css_selector(".basic-modal__title")
        if modal_form.__sizeof__()>0:
            driver.find_element_by_css_selector("button.y-button.y-button_theme_action.y-button_size_s.y-button_type_button").click()
        WebDriverWait(driver, 3).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class*='panel_visible designer-drawer__panel_animated']")))
    def click_by_yametrika(self, driver):
        yametrika_button = driver.find_element_by_xpath("//div[@role='button' and contains(.,'Яндекс.Метрика')]")
        driver.execute_script("arguments[0].click();",yametrika_button)
        if driver.find_elements_by_css_selector("div[class*='select_theme_normal']").__sizeof__()==0:
            yametrika_button.click()



    def configure_page(self, driver):
        ManagerApp.get_logger().info("Configure page")
        self.click_by_page_settings(driver)
        name_page_book = driver.find_element_by_css_selector(".lpc-text__input-wrapper > div > div > input")
        name_page_book.clear()
        name_page_book.send_keys("book")
        driver.find_element_by_xpath("//div[@role='button' and contains(.,'Поисковая оптимизация')]").click()
        driver.find_element_by_css_selector("textarea[name=comment]").send_keys(
            ManagerApp().get_json_data()["text"]["subtitle"])
        ManagerApp.get_logger().info("Click button settings page")
        self.click_by_save_settings(driver)
        ManagerApp.get_logger().info("Click by save button")
        #driver.find_element_by_css_selector(".y-button_theme_action.y-button_size_s.y-button_type_button").click()
        #driver.find_element_by_css_selector("div.page-settings__footer > button").click()

    def click_by_page_settings(self, driver):
        ManagerApp.get_logger().info("Click by \"Page settings\"")
        driver.find_element_by_xpath("//button[text()='Настройки страницы']").click()

    def click_by_site_settings(self, driver):
        ManagerApp.get_logger().info("Click by \"Site settings\"")
        driver.find_element_by_xpath("//button[@class='designer-drawer__item' and text()='Настройки сайта']").click()

    def save_and_publish_page(self, driver, page_name):
        # ManagerApp.get_logger().info("Click button \"Save\"")
        # driver.find_element_by_css_selector(".designer-header__group_align_right > span > button").click()
        # driver.find_element_by_xpath("//*[contains(.,'Все изменения сохранены')]")

        ManagerApp.get_logger().info("Click button \"Publish\"")
        # WebDriverWait(driver, 3).until(
        #     EC.invisibility_of_element_located((By.CSS_SELECTOR, "div[class*='panel_visible designer-drawer__panel_animated']")))
        self.click_by_publish(driver)
        ManagerApp.get_logger().info("Set pageUrl=" + page_name)
        page_domain = driver.find_element_by_css_selector(
            ".published-modal__content > div > div > div:nth-child(2) > div > div > div.lpc-text__input-wrapper > div > div > input")
        page_domain.send_keys(Keys.CONTROL + "a")
        page_domain.send_keys(Keys.DELETE)
        page_domain.send_keys(page_name)
        sleep(1)
        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_css_selector("button[class*='button_type_save']"))
        sleep(3)
        ManagerApp.get_logger().info("Close form")
        driver.execute_script("arguments[0].click();",
                              driver.find_element_by_css_selector("button[class*='closer-icon']"))

    def click_by_publish(self, driver):
        driver.find_element_by_css_selector("div.designer-header__button-wrapper > button").click()

    def click_by_good(self,driver):
        sleep(2)
        good_button = driver.find_element_by_xpath("//*[@class='modal__controls']//*[text()='Хорошо']")
        #WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.XPATH, good_button)))
        good_button.click()
    def configure_footer(self, driver):
        ManagerApp.get_logger().info("Configurate footer")
        ManagerApp.get_logger().info("Click by footer")
        #driver.find_element_by_xpath("//*[@class='panel-layer__label' and text()='Подвал']").click()
        #driver.find_element_by_css_selector("span[title='Подвал']").click()
        driver.execute_script("arguments[0].scrollIntoView();",
                              driver.find_element_by_css_selector("span[title='Подвал']"))
        sleep(3)
        driver.find_element_by_css_selector("span[title='Подвал']").click()
        ManagerApp.get_logger().info("Set info about company")
        driver.find_element_by_css_selector(
            "div > div > div > div.DraftEditor-editorContainer > div > div > div > div").send_keys(
            ManagerApp().get_json_data()["footer"]["about_company"])
        driver.find_element_by_css_selector("input[placeholder='Имя компании']").send_keys(
            ManagerApp().get_json_data()["footer"]["name_company"])
        driver.find_element_by_css_selector(
            ".menu-editor > div.control-block.lego-list.lego-list_can-add.lego-list_can-remove > div.lego-list__button-wrapper > button").click()
        driver.find_element_by_css_selector(".lego-list__item-viewer").click()
        menu_item_name = driver.find_element_by_css_selector("input[value='Пункт меню 1']")
        menu_item_name.send_keys(Keys.CONTROL + "a")
        menu_item_name.send_keys(Keys.DELETE)
        menu_item_name.send_keys(ManagerApp().get_json_data()["footer"]["menu_item_name"])
        driver.find_element_by_css_selector("input[placeholder='http://']").send_keys(
            ManagerApp().get_json_data()["footer"]["menu_item_url"])
        self.click_by_button_back(driver)
        self.add_social_media(driver, "Одноклассники", "ok")
        self.add_social_media(driver, "Telegram", "telegram")
        self.add_social_media(driver, "Вконтакте", "vk")
        self.add_social_media(driver, "Pinterest", "pinterest")
        self.add_social_media(driver,"YouTube", "youtube")

    def add_social_media(self, driver, social_type, name_parameter):
        ManagerApp.get_logger().info("Add social media")
        #"div[class*='list__item_invalid  invalid_control'"
        ManagerApp.get_logger().info("Click button \"Add social media\"")
        add_social_button = driver.find_element_by_css_selector(
            "div:nth-child(4) > div.control-block.lego-list.lego-list_can-add.lego-list_can-remove > div.lego-list__button-wrapper")
        add_social_button.click()
        driver.execute_script("arguments[0].scrollIntoView();",
                              add_social_button)
        driver.find_element_by_css_selector("div[class*='list__item_invalid  invalid_control'").click()
        driver.execute_script("arguments[0].scrollIntoView();",
                              driver.find_element_by_css_selector(".editor-block__header"))
        driver.find_element_by_css_selector("div > div.lp-lego-select-popup").click()
        driver.find_element_by_xpath("//span[@class='Menu-Text' and text()='%s']" % social_type).click()
        driver.find_element_by_css_selector(
            'div:nth-child(1) > div.lp-lego-input.lp-lego-input_empty.lp-lego-input_has-clear > div > span > input') \
            .send_keys(ManagerApp().get_json_data()["social"][name_parameter])
        self.click_by_button_back(driver)

    def add_buttons(self, driver):
        ManagerApp.get_logger().info("Add buttons")
        self.click_new_section_button(driver)
        buttons = driver.find_element_by_xpath("//span[@class='section-library__section-title' and text()='Кнопки']")
        driver.execute_script("arguments[0].scrollIntoView();", buttons)
        buttons.click()
        driver.find_element_by_css_selector(
            "div:nth-child(2) > div > div.section-library__preset.section-library__preset_has-title > div > div.drag-target > img").click()
        driver.find_element_by_xpath("//*[@class='lc-button-item-viewer' and text()='Оставить заявку']").click()
        name_button1 = driver.find_element_by_css_selector("input[class='Textinput-Control'][value='Оставить заявку']")
        name_button1.send_keys(Keys.CONTROL + "a")
        name_button1.send_keys(Keys.DELETE)
        name_button1.send_keys(ManagerApp().get_json_data()["buttons"]["button1_name"])
        url_button1 = driver.find_element_by_css_selector("input[class='Textinput-Control'][placeholder='http://']")
        url_button1.send_keys(Keys.CONTROL + "a")
        url_button1.send_keys(Keys.DELETE)
        url_button1.send_keys(ManagerApp().get_json_data()["buttons"]["button1_url"])
        self.click_by_button_back(driver)
        driver.find_element_by_xpath("//*[@class='lc-button-item-viewer' and text()='Узнать подробнее']").click()
        name_button2 = driver.find_element_by_css_selector("input[class='Textinput-Control'][value='Узнать подробнее']")
        name_button2.send_keys(Keys.CONTROL + "a")
        name_button2.send_keys(Keys.DELETE)
        name_button2.send_keys(ManagerApp().get_json_data()["buttons"]["button2_name"])
        url_button2 = driver.find_element_by_css_selector("input[class='Textinput-Control'][placeholder='http://']")
        url_button2.send_keys(Keys.CONTROL + "a")
        url_button2.send_keys(Keys.DELETE)
        url_button2.send_keys(ManagerApp().get_json_data()["buttons"]["button2_url"])

    def click_by_button_back(self, driver):
        driver.find_element_by_css_selector("div[class*=back-to-main-editor]").click()

    def add_full_description(self, driver):
        ManagerApp.get_logger().info("Add full description")
        self.click_new_section_button(driver)
        self.click_by_text_button(driver)
        driver.find_element_by_css_selector(
            "div:nth-child(8) > div > div.section-library__preset.section-library__preset_has-title > div > div.drag-target > img").click()
        driver.find_element_by_css_selector(
            ".lego-richtext__text_clearable > div > div > div > div > div > div > span > span").send_keys(
            ManagerApp().get_json_data()["text"]["full_description"])

    def add_photo(self, driver, path_photo, url):
        ManagerApp.get_logger().info("Add photo to block Graphic")
        self.click_new_section_button(driver)
        graphic = driver.find_element_by_xpath("//span[@class='section-library__section-title' and text()='Графика']")
        driver.execute_script("arguments[0].scrollIntoView();", graphic)
        graphic.click()
        driver.find_element_by_css_selector(
            "div:nth-child(2) > div > div.section-library__preset.section-library__preset_has-title > div > div.drag-target > img").click()
        driver.find_element_by_css_selector("input[type=file]").send_keys(path_photo)
        driver.find_element_by_css_selector(".lego-attach__thumbnail")
        driver.find_element_by_css_selector("[placeholder='http://'][class='Textinput-Control']").send_keys(url)


    def create_text_section(self, driver):
        ManagerApp.get_logger().info("Configuration block Text")
        self.click_new_section_button(driver)
        self.click_by_text_button(driver)
        text_section = driver.find_element_by_xpath("//*/div[9]//*[@class='section-library__preset-screen-wrapper']")
        driver.execute_script("arguments[0].scrollIntoView();", text_section)
        text_section.click()
        header_title = driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div:nth-child(1) > div.control-block.lego-richtext.lego-richtext_hasMaxLength.lego-richtext_isEmpty > div.lego-richtext__control > div.lego-richtext__text.lego-richtext__text_clearable > div > div.DraftEditor-editorContainer > div > div > div > div")
        header_title.send_keys(ManagerApp().get_json_data()["text"]["title"])
        subtitle = driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div:nth-child(2) > div.control-block.lego-richtext.lego-richtext_hasMaxLength.lego-richtext_isEmpty > div.lego-richtext__control > div.lego-richtext__text.lego-richtext__text_clearable > div > div.DraftEditor-editorContainer > div > div > div > div")
        subtitle.send_keys(ManagerApp().get_json_data()["text"]["subtitle"])
        description = driver.find_element_by_xpath(
            "//*[@class='notranslate public-DraftEditor-content']//*[contains(., 'описание')]")
        description.send_keys(Keys.CONTROL + "a")
        description.send_keys(Keys.DELETE)
        description.send_keys(ManagerApp().get_json_data()["text"]["description"])

    def click_by_text_button(self, driver):
        text_button = driver.find_element_by_xpath("//*[@class='section-library__section-title' and text()='Текст']")
        driver.execute_script("arguments[0].scrollIntoView();", text_button)
        text_button.click()

    def create_header_section(self, driver):
        self.click_new_section_button(driver)
        ManagerApp.get_logger().info("Configuration block Header")
        driver.find_element_by_xpath("//*[text()='Шапка']").click()
        driver.find_element_by_css_selector(
            "#app > div.designer > div.designer-drawer > div.designer-drawer__panel.designer-drawer__panel_visible.designer-drawer__panel_animated > div.designer-drawer__content > div.designer-drawer__item-content > div > div:nth-child(4) > div > div.section-library__preset.section-library__preset_has-title > div > div.drag-target > img").click()
        ManagerApp.get_logger().info("Remove fields")
        driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div.editor-block.menu-editor > div.control-block.lego-list.lego-list_has-items.lego-list_can-add.lego-list_can-remove > div.lego-list__container > div:nth-child(1) > div:nth-child(5) > span").click()
        driver.find_element_by_css_selector(
            "body > div.lp-lego-select-popup__popup.lp-lego-select-popup__popup_visible.lego-list__dropdown-actions > div > div:nth-child(4) > span > span").click()
        sleep(3)
        driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div.editor-block.menu-editor > div.control-block.lego-list.lego-list_has-items.lego-list_can-add.lego-list_can-remove > div.lego-list__container > div:nth-child(2) > div:nth-child(5) > span > svg").click()
        driver.find_element_by_css_selector(
            "body > div.lp-lego-select-popup__popup.lp-lego-select-popup__popup_visible.lego-list__dropdown-actions > div > div:nth-child(4) > span > span").click()
        sleep(1)
        driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div.editor-block.menu-editor > div.control-block.lego-list.lego-list_has-items.lego-list_can-add.lego-list_can-remove > div.lego-list__container > div:nth-child(1) > div:nth-child(5) > span > svg").click()
        driver.find_element_by_css_selector(
            "body > div.lp-lego-select-popup__popup.lp-lego-select-popup__popup_visible.lego-list__dropdown-actions > div > div:nth-child(4) > span > span").click()
        sleep(1)
        driver.find_element_by_css_selector(
            "#app > div.designer > div.designer__wrapper > div.designer-panel > div.designer-panel__content > div.designer-panel__tabs-wrapper > div.designer-panel__editor > div.editor-block.menu-editor > div.control-block.lego-list.lego-list_has-items.lego-list_can-add.lego-list_can-remove > div.lego-list__container > div > div:nth-child(5) > span > svg").click()
        driver.find_element_by_css_selector(
            "body > div.lp-lego-select-popup__popup.lp-lego-select-popup__popup_visible.lego-list__dropdown-actions > div > div:nth-child(4) > span > span").click()
        ManagerApp.get_logger().info("Set name company")
        name_company = driver.find_element_by_xpath("//*[@id='app']//*[@class='DraftEditor-editorContainer']")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(
            "//*[@class='control-block__label' and text()='Название компании']"))
        name_company.click()
        sleep(1)
        driver.find_element_by_class_name("lego-richtext__clear").click()
        driver.find_element_by_xpath("//*[@class='DraftEditor-root']//span/br").send_keys(
            ManagerApp().get_json_data()["header"]["name_company"])
        ManagerApp.get_logger().info("Set logo company")
        driver.find_element_by_css_selector("input[type=file]").send_keys(ManagerApp().get_json_data()["graphic"]["logo"])
        ManagerApp.get_logger().info("Set site url")
        driver.find_element_by_xpath("//*[@class='Textinput-Control' and @placeholder='https://']").send_keys(
            ManagerApp().get_json_data()["header"]["url_button"])
        ManagerApp.get_logger().info("Set name button")
        button_name = driver.find_element_by_xpath("//*[@class='Textinput-Control' and @placeholder='Перейти на сайт']")
        button_name.send_keys(Keys.CONTROL + "a")
        button_name.send_keys(Keys.DELETE)
        button_name.send_keys(ManagerApp().get_json_data()["header"]["name_button"])
        ManagerApp.get_logger().info("Set alternative url")
        driver.find_element_by_xpath("//*[@class='Textinput-Control' and @placeholder='http://']") \
            .send_keys(str(ManagerApp().get_json_data()["header"]["url_button"]).replace("https", "http"))

    def switch_to_frame(self, driver):
        frame = driver.find_element_by_xpath(
            "//*[@class='i-foreign-iframe p-show-turbo-landings__iframe i-bem i-foreign-iframe_js_inited']")
        driver.switch_to.frame(frame)










