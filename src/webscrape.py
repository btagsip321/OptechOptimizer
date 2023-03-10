from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import pdb
import os
import re

scraper = webdriver.Firefox()
pc_parts = {}

parts = {
    "GPU": "https://gpu.userbenchmark.com/",
    "CPU": "https://cpu.userbenchmark.com/",
    "SSD": "https://ssd.userbenchmark.com/",
    "HDD": "https://hdd.userbenchmark.com/",
    "RAM": "https://ram.userbenchmark.com/",
}

def fetch_price(row):
    scraper.get(row['URL'])
    price = 0

    try:
        price_button = scraper.find_element(By.CLASS_NAME, "nowrap")
        price = float(re.sub("[^0-9]", "", price_button.text))
        if price <= 10000:
            print(price)
        else:
            price = 0
            print("Price too high / DNE, setting to 0")

    except:
        print("Failed to get price")
    
    return price

for part, url in parts:
    #csv = pd.DataFrame(columns = ['Name', 'Price', 'Market Share'])

    scraper.get(url)
    mytable = scraper.find_element(By.CSS_SELECTOR, '#tableDataForm\:mhtddyntac > table')
    for row in mytable.find_element(By.CSS_SELECTOR, 'tr'):
        for cell in row.find_element(By.TAG_NAME, 'td'):
            print(cell.text)

    #csv.to_csv()

#pdb.set_trace()