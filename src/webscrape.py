from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
import pandas as pd
import time
import pdb
import os
import re
import glob

# Lets heroku use the selenium webdriver
if os.environ.get("CHROMEDRIVER_PATH"):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    SCRAPER = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
else:
    SCRAPER = webdriver.Chrome()

# Now you can start using Selenium

# List of parts to loop through, with the part category as the key and the URL as the value
PARTS = {
    "GPU": ["https://gpu.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":7, "URL":None}],
    "CPU": ["https://cpu.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9, "URL":None}],
    "RAM": ["https://ram.userbenchmark.com/", {"Rank":0, "Name":1, "Capacity":2, "Benchmark":5, "Price":10, "URL":None}],
    "SSD": ["https://ssd.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9, "URL":None, "Capacity":5}],
    "HDD": ["https://hdd.userbenchmark.com/", {"Rank":0, "Name":1, "Benchmark":4, "Price":9, "URL":None, "Capacity":5}],
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
    
print('Cleaning data folder...')
for filename in os.listdir('../data'):
    if filename != "CASE.csv":
        print(os.path.join('../data', filename))
        os.remove(os.path.join('../data', filename))

print("Scraping data...")

# Loop through each part
for part in PARTS:

    #Create a pd dataframe to be turned into a CSV
    index = PARTS[part]
    url, format = index[0], index[1]
    csv = pd.DataFrame(columns = format.keys())

    # Send a get request to URL
    SCRAPER.get(url)
    time.sleep(4)

    # Open up capacity for ram
    #if part == "RAM":
        #SCRAPER.find_element(By.CSS_SELECTOR, "#tableDataForm\:mhtddyntac > table > thead > tr > th:nth-child(11) > a").click()
        #SCRAPER.find_element(By.CSS_SELECTOR, "#columnsDialog > div > div > div.modal-body > div > a:nth-child(1)").click()
        #SCRAPER.find_element(By.CSS_SELECTOR, "#columnsDialog > div > div > div.modal-header > button").click()

    # Sort scraper by price
    button = SCRAPER.find_element(By.CSS_SELECTOR, '[data-mhth=MC_PRICE]')
    SCRAPER.execute_script("$(arguments[0]).click();", button)
    SCRAPER.execute_script("$(arguments[0]).click();", button)

    # Loop through all iterations
    for i in range(0, ITERATIONS):

        # Loop through table elements
        mytable = SCRAPER.find_element(By.CSS_SELECTOR, '#tableDataForm\:mhtddyntac > table')
        for row in mytable.find_elements(By.CSS_SELECTOR, 'tr'):
            elements = row.find_elements(By.TAG_NAME, 'td')
            if len(elements) > 0:

                print(elements[format["Benchmark"]].text.split("\n")[0])

                # Initiate new row variable
                newRow = [
                    int(elements[format["Rank"]].text), #Rank
                    elements[format["Name"]].text.split("\n")[1], #Name
                    float(elements[format["Benchmark"]].text.split("\n")[0]), #Benchmark
                    fetch_price(elements[format["Price"]].text), #Price
                    elements[format["Name"]].find_element(By.CLASS_NAME, "nodec") .get_attribute("href") # URL
                ]

                # Capacity, only for RAM, SSD and HDD
                if (part == "RAM" or part == "HDD" or part == "SSD"):
                    capacity = fetch_capacity(elements[format["Capacity"]].text)
                    newRow.append(capacity)

                # Add row to the csv dataframe
                csv.loc[len(csv.index)] = newRow

        # Click the next button to go through next page on the table
        SCRAPER.find_element(By.CSS_SELECTOR, "#tableDataForm\:j_idt200").click()
        time.sleep(4)
        
    # Create new CSV file
    file = open("../data/" + part + ".csv", "a")
    file.write(csv.to_csv(encoding='utf-8', index=False))
    file.close()