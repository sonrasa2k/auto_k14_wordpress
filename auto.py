from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pyautogui
ULR = "https://vnshowbiz.net/wp-admin"

driver = webdriver.Chrome("chromedriver.exe")
driver.get(ULR)

user = driver.find_element_by_name("log")
pwd = driver.find_element_by_name("pwd")
button = driver.find_element_by_name("wp-submit")
user.send_keys("honghue")
pwd.send_keys("honghue12t@gmail.com")
button.click()
time.sleep(3)
driver.get("https://vnshowbiz.net/wp-admin/post-new.php")
check_point = driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div[2]/button")
check_point.click()
check_point.click()
check_point.click()
check_point=driver.find_element_by_xpath("/html/body/div[5]/div/div/div/div/div/div/div/div[2]/div[2]/button[2]")
check_point.click()
title = driver.find_element_by_xpath('//*[@id="post-title-0"]')
title.send_keys("son dep trai")
title.send_keys("\n")
content = driver.find_element_by_css_selector("p.wp-block")
content.send_keys("son bao dep trai")
tai_lieu = driver.find_element_by_xpath('//*[@id="editor"]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/ul/li[1]/button')
tai_lieu.click()
anh_dai_dien = driver.find_element_by_xpath('//*[@id="editor"]/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div[5]/h2/button')
anh_dai_dien.click()
chon_anh = driver.find_element_by_xpath('//*[@id="editor"]/div/div/div[1]/div/div[2]/div[2]/div/div[3]/div[5]/div/div/button')
chon_anh.click()
button_test = driver.find_element_by_class_name('attachment save-ready selected details')
button.click()

# upload_file = driver.find_element_by_xpath('//*[@id="menu-item-upload"]')
# upload_file.click()
# time.sleep(2)
# file_final = driver.find_element_by_xpath('//*[@id="__wp-uploader-id-1"]')
# file_final.click()
# input_file = "//input[starts-with(@id,'html5_')]"
# driver.find_element_by_xpath(input_file).send_keys(r'C:\Users\sonng\auto_dangbai\docker.png')
# dang_anh = driver.find_element_by_xpath('//*[@id="__wp-uploader-id-0"]/div[4]/div/div[2]/button')
# dang_anh.click()
# dang_anh.click()
# time.sleep(10)
# driver.close()


