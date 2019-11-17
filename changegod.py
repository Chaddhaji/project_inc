from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2 
})


driver = webdriver.Chrome(\
    executable_path=r'.\chromedriver_win32\chromedriver.exe',\
    chrome_options=chrome_options)

driver.get("https://changegod.com/greenseed_yt_test47.html")
time.sleep(1)

driver.switch_to.frame(driver.find_element_by_xpath('//iframe[starts-with(@src, "https://bit")]'))
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Play"]'))).click()