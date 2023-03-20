from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import pdb
import os
import re
import glob

# Selenium web driver scraper. Uses firefox since this is the only browser that works on my laptop
SCRAPER = webdriver.Chrome()

# List of parts to loop through, with the part category as the key and the URL as the value
PARTS = {
    "GPU": ["https://gpu.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":7}],
    "CPU": ["https://cpu.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9}],
    "RAM": ["https://ram.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9}],
    "SSD": ["https://ssd.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9, "Capacity":5}],
    "HDD": ["https://hdd.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9, "Capacity":5}],
}

# Number of iterations, amount of entries = 50 + iterations*50
ITERATIONS = 2

# Attempts to fetch the price
# If it fails to do so, returns -1 to signal an error
def fetch_price(raw_price):
    try:
        return int(raw_price.split("\n")[0][1:].replace(",",""))
    except:
        return -1
    
# Attempts to fetch the capacity, converts to GB
def fetch_capacity(raw_capacity):
    capacity = raw_capacity.split("\n")[0]
    return int(''.join(i for i in capacity if i.isdigit())) * (1000 if "TB" in raw_capacity else 1)
        
print("Scraping data...")

# Loop through each part
for part in PARTS:

    #Create a pd dataframe to be turned into a CSV
    index = PARTS[part]
    url, format = index[0], index[1]
    csv = pd.DataFrame(columns = format.keys())

    # Send a get request to URL
    SCRAPER.get(url)

    # Loop through all iterations
    for i in range(0, ITERATIONS):

        # Loop through table elements
        mytable = SCRAPER.find_element(By.CSS_SELECTOR, '#tableDataForm\:mhtddyntac > table')
        for row in mytable.find_elements(By.CSS_SELECTOR, 'tr'):
            elements = row.find_elements(By.TAG_NAME, 'td')
            if len(elements) > 0:

                print(elements[format["Rank"]].text)
                print(elements[format["Benchmark"]].text)
                # Initiate new row variable
                newRow = [
                    int(elements[format["Rank"]].text), #Rank
                    elements[format["Name"]].text.split("\n")[1], #Name
                    int(elements[format["Benchmark"]].text), #Benchmark
                    fetch_price(elements[format["Price"]].text), #Price
                ]
                print(elements[format["Name"]].get_attribute("href"))

                # Capacity, only for SSD and HDD
                if (part == "SSD" or part == "HDD"):
                    capacity = fetch_capacity(elements[format["Capacity"]].text)
                    newRow.append(capacity)

                # Add row to the csv dataframe
                csv.loc[len(csv.index)] = newRow

        # Click the next button to go through next page on the table
        SCRAPER.find_element(By.CSS_SELECTOR, "#tableDataForm\:j_idt274").click()
        time.sleep(4)
        
    # Create new CSV file
    file = open("../data/" + part + ".csv", "a")
    file.write(csv.to_csv(encoding='utf-8', index=False))
    file.close()