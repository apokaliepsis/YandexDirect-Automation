from manager_app import *
from login import *
from direct_main import *
from metrika import *


def run_app():
    ManagerApp.get_logger().info("Start app")
    #Login().authorize()
    Login().open_direct_page()
    ManagerApp().addCookies()
    DirectMain().open_yadirect()
    DirectMain().create_turbopage()
    driver = ManagerApp().get_driver()

    name_counter = Metrika().createMetrika()
    driver.switch_to.window(driver.window_handles[0])
    DirectMain().switch_to_frame(driver)
    DirectMain().add_counter_to_page(driver, name_counter)
    DirectMain().click_by_publish(driver)
    driver.switch_to.window(driver.window_handles[1])
    Metrika().create_goals()
    #BaseDriver().quitDriver()




if __name__ == '__main__':
    run_app()