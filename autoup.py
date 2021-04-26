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
        #self.driver.set_window_position(-10000, 0)
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
        check_point = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div/div/div[2]/div[2]/button")
        check_point.click()
        check_point.click()
        check_point.click()
        check_point = self.driver.find_element_by_xpath("/html/body/div[6]/div/div/div/div/div/div[2]/div[2]/button[2]")
        check_point.click()
        title_point = self.driver.find_element_by_xpath('//*[@id="post-title-0"]')
        title_point.send_keys(title)
        title_point.send_keys("\n")
        content_point = self.driver.find_element_by_css_selector("p.wp-block")
        content_point.send_keys(Keys.CONTROL, 'v')
        time.sleep(3)
        upload_button = self.driver.find_element_by_xpath('//*[@id="editor"]/div[1]/div/div[1]/div/div[2]/button[2]')
        upload_button.click()
        time.sleep(2)
        check_point2 = self.driver.find_element_by_xpath('//*[@id="editor"]/div[1]/div/div[2]/div[3]/div[3]/div/div/div[1]/div[1]/button')
        check_point2.click()
        time.sleep(3)
        link_bai_viet_dang = self.driver.page_source.split('Bài viết đã được đăng.<a href="')[1].split('" class="')[0]
        with open('link_da_dang.txt','a+',encoding='utf-8') as f:
            f.write(link_bai_viet_dang+"\n")
        self.driver.quit()
        return "Đăng bài thành công ♥"