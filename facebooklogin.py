from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from datetime import timedelta
import time

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})

username = "bigboss@itymail.com"
password = "bigboss@123"

driver = webdriver.Chrome(\
    executable_path=r'.\chromedriver_win32\chromedriver.exe',\
    chrome_options=chrome_options)

driver.get("https://www.facebook.com/")
time.sleep(1)

emailfield = driver.find_element_by_id("email")
pwdfield = driver.find_element_by_id("pass")
loginButton = driver.find_element_by_id("loginbutton")

emailfield.send_keys(username)
pwdfield.send_keys(password)
loginButton.click()

