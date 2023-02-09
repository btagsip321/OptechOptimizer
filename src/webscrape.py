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

for file in os.scandir("../data"):
    if file.is_file():
        print("Getting " + file.name)
        pc_parts[file.name] = pd.read_csv(file.path).sort_values(by=['Benchmark'], ascending=False).head(50)
        pc_parts[file.name]['Price'] = pc_parts[file.name].apply(lambda row: fetch_price(row), axis = 1)

pdb.set_trace()