from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
class AutoUp:
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--hide-scrollbars')
        options.add_argument('--disable-gpu')
        options.add_argument("--log-level=3")  # fatal
        self.driver = webdriver.Chrome("chromedriver.exe",options=options)
        self.driver.set_window_position(-10000, 0)
    def login(self,URL_Login_Wp,user_name, passwd):
        self.driver.get(URL_Login_Wp)
        user = self.driver.find_element_by_name("log")
        pwd = self.driver.find_element_by_name("pwd")
        submit = self.driver.find_element_by_name("wp-submit")
        user.send_keys(user_name)
        pwd.send_keys(passwd)
        submit.click()
        time.sleep(3)
        return "Login Thành Công"
    def Auto_UpPost(self,URL_upload,title,content):
        self.driver.get(URL_upload)
        check_point = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div[2]/button")
        check_point.click()
        check_point.click()
        check_point.click()
        check_point = self.driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div[2]/button[2]")
        check_point.click()
        title_point = self.driver.find_element_by_xpath('//*[@id="post-title-0"]')
        title_point.send_keys(title)
        title_point.send_keys("\n")
        content_point = self.driver.find_element_by_css_selector("p.wp-block")
        content_point.send_keys(Keys.CONTROL, 'v')
        time.sleep(3)
        upload_button = self.driver.find_element_by_css_selector("#editor > div > div > div.components-navigate-regions > div > div.interface-interface-skeleton__header > div > div.edit-post-header__settings > button.components-button.editor-post-publish-panel__toggle.editor-post-publish-button__button.is-primary")
        upload_button.click()
        time.sleep(2)
        check_point2 = self.driver.find_element_by_css_selector("#editor > div > div > div.components-navigate-regions > div > div.interface-interface-skeleton__body > div.interface-interface-skeleton__actions > div > div > div > div.editor-post-publish-panel__header > div.editor-post-publish-panel__header-publish-button > button")
        check_point2.click()
        time.sleep(3)
        self.driver.quit()
        return "Đăng bài thành công ♥"