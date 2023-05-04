import pandas as pd
import json
import pdb
import os
import re

parts = ['CPU','GPU','HDD','RAM','SSD','CASE']
cpuMax = 1400
gpuMax = 1800

pc_parts = {'CPU':None, 'GPU':None, 'HDD':None, 'RAM':None, 'SSD':None, 'CASE':None}
#Rounds budget to 2 decimal places
def cleanBudget(budget, minBudget =0, maxBudget =50000):
    try:
        # Make budget in between min budget and max budget, round to 2 decimal plaecs
        return max(minBudget, min(round(budget, 2), maxBudget))

    except:
        return 0

def buildBudget(budget, windows = False, tax = 0):

    # add tax to budget
    budget = (budget)/((1) + (tax/100))
   
    # subtract 100 from budget if windows, else subtract 0
    subtr = (140 if windows else 0)
    budget -= subtr

    print("Calculated Tax: ", ((1) + (tax/100)))
    print("Tax: ", tax)
    print("New Budget:", budget)

    # if 5% of budget is less than 45, spend 45, else spend 5% of budget
    if ((budget * .05) < 45):
        budget -= 45
        caseMoney = 45
    else:
        caseMoney = round((budget * .05), 2)

    # if 5.1% of budget is less than 51, spend 51, else spend 5.1% of budget
    if ((budget * .051 < 51)):
        budget -= 51
        ssdMoney = 51
    else:
        ssdMoney = round((budget * .051), 2)
        
    if((budget * .331 > gpuMax)):
        gpuMoney = gpuMax
    elif((budget * .331 > 1200)):
        gpuMoney = 1200
    elif((budget * .331 > 850)):
        gpuMoney = 850
    else:
        gpuMoney = budget * .331
        
    if((budget * .262 > cpuMax)):
        cpuMoney = cpuMax
    elif((budget * .262 > 600)):
        cpuMoney = 600
    else:
        cpuMoney = budget * .262
    budget = budget - gpuMoney - cpuMoney
    
    # clean budget between 800 and 50000
    #budget = cleanBudget(budget, 800, 50000)

    allocation = {
        #"Windows Key": subtr,
        "GPU": cleanBudget((gpuMoney), 0, 50000),
        "CPU": cleanBudget((cpuMoney), 0, 50000),
        "RAM": cleanBudget((budget * 0.2058)),
        "CASE": cleanBudget((caseMoney), 0, 50000),
        "PSU": cleanBudget((budget * 0.204), 0, 140),
        "SSD": cleanBudget((ssdMoney), 0, 50000),
        "HDD": cleanBudget((budget * 0.15)),
        "Motherboard": cleanBudget((budget * .3447), 0, 200),
        "CPU Cooler": cleanBudget((budget * .0955), 0, 300),
    }

    return allocation

def gatherPartData(part):
    path = os.path.join('./data/', part + '.csv')
    df = pd.read_csv(path).dropna()
    pc_parts[part] = df[df.Price != -1]
    
def findPartsWithinBudget(part, budget, preferredBrand, ssdStorageSpace, hddStorageSpace):
    part_data = pc_parts[part]

    # Filter by brand
    if preferredBrand:
        part_data = part_data[part_data["Name"].str.contains(preferredBrand)]
    
    # Filter by storage space
    if ssdStorageSpace:
        part_data = part_data[part_data["Capacity"].astype(int) >= ssdStorageSpace]
    if hddStorageSpace:
        part_data = part_data[part_data["Capacity"].astype(int) >= hddStorageSpace]
    
    # Filter by price and highest benchmark
    part_data = part_data[part_data["Price"] <= budget]

    # Sort by benchmark
    if part == "CASE":
        part_data = part_data.sort_values(['Rank'], ascending = [True])
    else:
        part_data = part_data.sort_values(['Benchmark'], ascending = [False])
    
    display = part_data.iloc[0]['Name']

    # Add price if not already in name
    if not ("$" in display):
        display = display + " $" + str(part_data.iloc[0]['Price'])

    # Add URL if not already in name
    display = display + " Buy here: " + part_data.iloc[0]['URL']

    return display

def extractPrice(price):
    extract = re.search("(?:[\£\$\€]{1}[,\d]+.?\d*)", price)
    return float(extract.group().replace("$", "").replace(",", ""))

def buildPc(budget, cpu, ssdStorageSpace, hddStorageSpace):
    print(budget)
    pc = {
        "GPU": findPartsWithinBudget("GPU", budget["GPU"], None, None, None),
        "CPU": findPartsWithinBudget("CPU", budget["CPU"], cpu, None, None),
        "RAM": findPartsWithinBudget("RAM", budget["RAM"], None, None, None),
        "CASE": findPartsWithinBudget("CASE", budget["CASE"], None, None, None),
        #"PSU": findPartsWithinBudget("power-supply", budget["PSU"]),
        "PSU": "$" + str(budget["PSU"]) + " (Input budget into PC Part Picker)",
        "SSD": findPartsWithinBudget("SSD", budget["SSD"], None, ssdStorageSpace, None),
        "HDD": findPartsWithinBudget("HDD", budget["HDD"], None, None, hddStorageSpace),
        "Motherboard": "$" + str(budget["Motherboard"]) + " (Input budget into PC Part Picker)",
        "CPU_Cooler": "$" + str(budget["CPU Cooler"]) + " (Input budget into PC Part Picker)",
        #"Motherboard": findPartsWithinBudget("motherboard", budget["Motherboard"]),
        #"CPU Cooler": findPartsWithinBudget("cpu-cooler", budget["CPU Cooler"]),
    }

    price = sum(map(extractPrice, pc.values())) 
    pc["Total_Price"] = "$" + str(round(price, 2))

    return pc, price

for part in parts:
    print("Gathering part data for", part)
    gatherPartData(part)
