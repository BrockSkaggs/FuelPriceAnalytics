import csv
import datetime as dt
from dotenv import load_dotenv
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from typing import List
import traceback

from gmail_util import send_mail
load_dotenv()

data_file_path = 'gas-scrape-data.csv'
errors_path = 'scrape_errors.txt'
update_address = os.environ.get('email_update')

def main():
    print('running main...')
    scrape_results = []
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument("--window-size=1920,1080") #Helps with React dropdown. 
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(15)
        driver.get("https://www.gasbuddy.com/gasprices/missouri/carthage")
        run_time = dt.datetime.now()
        for fuel_type in ['regular', 'diesel', 'premium']:
            toggle_fuel_type(fuel_type, driver)
            fuel_type_info = review_panels(driver, fuel_type, run_time)
            scrape_results.append(fuel_type_info)
        send_mail(update_address, 'Fuel Scrape - Success', json.dumps(scrape_results, indent=6))
    except Exception as ex:
        record_error()
        send_mail(update_address, 'Fuel Scrape - Error', traceback.format_exc())
    print("done")

def review_panels(driver, fuel_type: str, run_time: dt.datetime) -> list:
    panels = locate_panels(driver)
    print(fuel_type)
    panel_infos = []
    pos = 1
    for panel in panels:
        panel_info = scrape_panel(panel)
        panel_info['position'] = pos
        panel_infos.append(panel_info)
        pos += 1
    record_panel_data(panel_infos, fuel_type, run_time)
    return panel_infos

def locate_panels(driver):
    card_class = "GenericStationListItem-module__station___1O4vF"
    return driver.find_elements(By.CLASS_NAME, card_class)

def scrape_panel(panel):
    station = panel.find_element(By.TAG_NAME, "H3").text.strip()
    address = panel.find_element(By.CLASS_NAME, "StationDisplay-module__address___2_c7v").text.strip()
    raw_price = panel.find_element(By.CLASS_NAME, "StationDisplayPrice-module__price___3rARL").text.strip()
    cond_price = float(raw_price.replace('$', '')) if '$' in raw_price else None
    return {
        'station': station,
        'address': address.replace('\n', '|'),
        'raw_price': raw_price, 
        'cond_price': cond_price
    }

def toggle_fuel_type(fuel_type: str, driver):
    type_toggle_btn = driver.find_element(By.CLASS_NAME, "Dropdown__toggle___11YIe")
    type_toggle_btn.click()
    drp_dwn = driver.find_element(By.CLASS_NAME, "Dropdown__optionBox___1Wt6d")
    drp_dwn_opts = drp_dwn.find_elements(By.TAG_NAME, "li")
    for opt in drp_dwn_opts:
        if fuel_type.lower() in opt.get_attribute("innerHTML").lower():
            opt.click()
            exit

def record_panel_data(panel_data: List[dict], fuel_type: str, run_time: dt.datetime):
    with open(data_file_path, 'a', newline='') as data_file:
        field_names = ['run_time', 'position', 'fuel_type', 'station', 'address', 'raw_price', 'cond_price']
        writer = csv.DictWriter(data_file, field_names, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
        cond_time = run_time.strftime("%Y-%m-%d %H:%M:%S")
        for panel in panel_data:
            panel['fuel_type'] = fuel_type
            panel['run_time'] = cond_time
            writer.writerow(panel)

def record_error():
    with open(errors_path, 'a') as err_file:
        err_file.write(f"Error Date: {dt.datetime.now()}")
        err_file.write(traceback.format_exc())

if __name__ == '__main__':
    main()