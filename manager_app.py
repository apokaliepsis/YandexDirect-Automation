import json
import os
import time
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import logging
import sys
import pickle


class ManagerApp:
    __driver: webdriver = None
    log: logging = None
    json_data: json = None
    #path_settings_file = sys.argv[1]
    path_settings_file = os.getcwd()+'/settings.json'

    def startDriver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--window-size=1920,1080")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--profile-directory=Default")
        # chrome_options.add_argument("--disable-plugins-discovery")
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.__driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), chrome_options=chrome_options)
        self.__driver.implicitly_wait(15)
        self.get_logger().info("session_id: "+self.__driver.session_id)
        self.get_logger().info("url: "+self.__driver.command_executor._url)

        return self.__driver

    def addCookies(self):
        cookies = pickle.load(open("cookies_ak.adv.2.pkl", "rb"))
        for cookie in cookies:
            self.__driver.add_cookie(cookie)

    def get_driver(self):
        if ManagerApp.__driver is None:
            print("Driver is null")
            ManagerApp.__driver = self.startDriver()
        return ManagerApp.__driver

    def quitDriver(self):
        ManagerApp.__driver.quit()

    def get_logger(name=__file__, file='log.txt', encoding='utf-8'):
        if ManagerApp.log is None:
            ManagerApp.log = logging.getLogger(name)
            ManagerApp.log.setLevel(logging.DEBUG)

            formatter = logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s %(message)s')

            fh = logging.FileHandler(file, encoding=encoding)
            fh.setFormatter(formatter)
            ManagerApp.log.addHandler(fh)

            sh = logging.StreamHandler(stream=sys.stdout)
            sh.setFormatter(formatter)
            ManagerApp.log.addHandler(sh)

        return ManagerApp.log
    def get_json_data(self):
        if ManagerApp.json_data is None:
            with open(ManagerApp.path_settings_file) as f:
                ManagerApp.json_data = json.load(f)
        return ManagerApp.json_data
