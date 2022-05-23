from manager_app import ManagerApp
class Login:
    def open_direct_page(self):
        ManagerApp().get_driver().get("https://direct.yandex.ru/")
    def authorize(self):
        ManagerApp.get_logger().info("Start authorization")
        driver = ManagerApp().get_driver()
        driver.get("https://passport.yandex.ru/auth?retpath=https%3A%2F%2Fdirect.yandex.ru%2F&origin=direct")
        # if driver.find_elements_by_class_name("AuthLoginInputToggle-type"):
        #     print("Element exists")
        #     driver.find_element_by_class_name("AuthLoginInputToggle-type").click()
        driver.find_element_by_xpath("//*[@class='Textinput-Control']").send_keys("ak.adv.2@yandex.ru")
        driver.find_element_by_xpath("//*[@type='submit']").click()
        driver.find_element_by_xpath("//*[@type='password' and @name='passwd']").send_keys("test2022")
        driver.find_element_by_xpath("//*[@type='submit']").click()
        driver.find_element_by_xpath("//*[@class='lc-styled-text']").click()