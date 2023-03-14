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

def fetch_price(raw_price):
    try:
        return int(raw_price.split("\n")[0][1:].replace(",",""))
    except:
        return -1



for part in parts:
    csv = pd.DataFrame(columns = ['Rank', 'Name', 'Price'])

    scraper.get(parts[part])
    mytable = scraper.find_element(By.CSS_SELECTOR, '#tableDataForm\:mhtddyntac > table')
    for row in mytable.find_elements(By.CSS_SELECTOR, 'tr'):
        elements = row.find_elements(By.TAG_NAME, 'td')
        if len(elements) > 0:
            csv.loc[len(csv.index)] = [
                int(elements[0].text),
                elements[1].text.split("\n")[1],
                fetch_price(elements[7].text)
            ]
    print(csv)
    #csv.to_csv()

#pdb.set_trace()