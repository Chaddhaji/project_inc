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
    options=chrome_options)

driver.get("https://www.sonyliv.com/")

got_video_list = False

while not got_video_list:
    current_height = driver.execute_script('return document.documentElement.offsetHeight+document.documentElement.scrollTop')
    scroll_height =  driver.execute_script('return document.body.scrollHeight')

    if current_height == scroll_height:
        got_video_list = False
        break
    else:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        except:
            pass

    videolist = driver.find_elements_by_xpath('//div[@class="owl-item"]')
    if len(videolist) > 10:
        got_video_list = True

selectedVideo = videolist[3].find_element_by_tag_name('a')
driver.execute_script("arguments[0].click();", selectedVideo)
time.sleep(1)

current_time = 0
while current_time == 0:
    try:
        current_time = driver.execute_script('return document.getElementsByTagName("Video")[0].currentTime')
        print("Ads is running")
    except:
        pass


print(current_time)
updated_time = int(current_time) + 100.0
driver.execute_script('return document.getElementsByTagName("Video")[0].currentTime={0}'.format(updated_time))
driver.execute_script('return document.getElementsByTagName("Video")[0].play()')

# driver.close()