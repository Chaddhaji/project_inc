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


driver = webdriver.Chrome(\
    executable_path=r'.\chromedriver_win32\chromedriver.exe',\
    chrome_options=chrome_options)


def expand_shadow_element(element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot',element)
  return shadow_root
  

driver.get("https://www.wego.co.in/")

##### HOME PAGE 

makalu_app = driver.find_element_by_tag_name('makalu-app')
shadow_makalu_app = expand_shadow_element(makalu_app)

wego_search_form = shadow_makalu_app.find_element_by_tag_name('wego-search-form')
shadow_wego_search_form = expand_shadow_element(wego_search_form)

wego_flight_search_form = shadow_wego_search_form.find_element_by_tag_name('wego-flight-search-form')
shadow_wego_flight_search_form = expand_shadow_element(wego_flight_search_form)

## SELECT WAY-TYPE
whatway = shadow_wego_flight_search_form.find_elements_by_class_name("triptype")
"""
whatway[0].click() #ONE WAY
whatway[1].click() #ROUND WAY
whatway[2].click() #MULTI CITY

#ONE WAY SELECTED BY DEFAULT
"""
###### SELECT LOCATION

### FROM LOCATION
dep_root = shadow_wego_flight_search_form.find_element_by_id("dep")
dep_shadow = expand_shadow_element(dep_root)
dep_root.click()

dep_result_box = dep_shadow.find_element_by_tag_name("result-box")
dep_result_box_shadow = expand_shadow_element(dep_result_box)


time.sleep(1)
location_list = dep_result_box_shadow.find_elements_by_class_name("location")

location_list[14].click() ##DELHI SELECTED



### TO LOCATION
arr_root = shadow_wego_flight_search_form.find_element_by_id("arr")
arr_shadow = expand_shadow_element(arr_root)
arr_root.click()

arr_result_box = arr_shadow.find_element_by_tag_name("result-box")
arr_result_box_shadow = expand_shadow_element(arr_result_box)

time.sleep(1)
location_list = arr_result_box_shadow.find_elements_by_class_name("location")

location_list[0].click() ##ABU DHABI SELECTED


## SELECT DATE
datefield = shadow_wego_flight_search_form.find_element_by_id('dates')
datefield.click()
shadow_datefield = expand_shadow_element(datefield)

time.sleep(0.5)
calendar_popup = shadow_datefield.find_element_by_tag_name('calendar-popup')
shadow_calendar_popup = expand_shadow_element(calendar_popup)

todaydate = datetime.now().date()+timedelta(days=5)
todaydate = todaydate.strftime('%d-%B-%Y')
monthlists = shadow_calendar_popup.find_elements_by_class_name('month')

select_date = None
for monthdiv in monthlists:
    date_found = False
    monthname, year = monthdiv.find_element_by_xpath('span[@class="month-name"]').text.split()
    daylist = [x for x in monthdiv.find_elements_by_class_name('day') if x.text]
    for day in daylist:
        tempdate = "{0}-{1}-{2}".format(day.text,monthname,year)
        if tempdate == todaydate:
            select_date = day
            break
    if select_date:
            break

assert select_date ##Throw error if date empty

select_date.click()

## SEARCH
search_root = shadow_wego_flight_search_form.find_element_by_id("search")
search_root.click()


window_after = driver.window_handles[-1]
driver.switch_to.window(window_after)

##### FLIGHT SEARCH LIST
gotit = False
while not gotit:
    time.sleep(1)
    makalu_app = driver.find_element_by_tag_name('makalu-app')
    shadow_makalu_app = expand_shadow_element(makalu_app)


    flights_search = shadow_makalu_app.find_element_by_id('flights-search')
    shadow_flights_search = expand_shadow_element(flights_search)

    flightResultList = shadow_flights_search.find_element_by_id('flightResultList')
    shadow_flightResultList = expand_shadow_element(flightResultList)


    listview = shadow_flightResultList.find_element_by_id('listview')
    # shadow_listview = expand_shadow_element(listview)

    flight_card_list = listview.find_elements_by_tag_name('flight-card')

    if flight_card_list:
        gotit = True

assert flight_card_list

flight_card_list = [flight_card_list[0]] ##Only looping through one card

for flight_card in flight_card_list:
    temp_shadow_flight_card = expand_shadow_element(flight_card)
    wego_button = temp_shadow_flight_card.find_element_by_tag_name("wego-button")
    wego_button.click()


    gotit = False
    while not gotit:
        time.sleep(1)
        makalu_app = driver.find_element_by_tag_name('makalu-app')
        shadow_makalu_app = expand_shadow_element(makalu_app)

        flight_detail = shadow_flights_search.find_element_by_tag_name("flight-detail")
        shadow_flight_detail = expand_shadow_element(flight_detail)

        flight_detail_fare_list = shadow_flight_detail.find_elements_by_tag_name("flight-detail-fare")

        if flight_detail_fare_list:
            gotit = True

    assert flight_detail_fare_list

    flight_detail_fare_list = [flight_detail_fare_list[0]] ##Only looping through one offer

    for flight_detail_fare_item in flight_detail_fare_list:
        print(flight_detail_fare_item)
        shadow_flight_detail = expand_shadow_element(flight_detail_fare_item)
        viewdeallink = shadow_flight_detail.find_element_by_tag_name('a')
        viewdeallink.click()
    
driver.close()
