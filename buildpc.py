import pandas as pd
import json
import pdb
import os

parts = ['CPU','GPU','HDD','RAM','SSD','CASE']
pc_parts = {'CPU':None, 'GPU':None, 'HDD':None, 'RAM':None, 'SSD':None, 'CASE':None}

def cleanBudget(budget, minBudget =0, maxBudget =1000):
    try:
        return max(minBudget, min(round(budget, 2), maxBudget))
    except:
        return 0

def buildBudget(budget, windows = False):
    subtr = (100 if windows else 10)
    budget -= subtr

    if ((budget * .05) < 45):
        budget -= 45
        caseMoney = 45
    else:
        caseMoney = round((budget * .05), 2)

    if ((budget * .051 < 51)):
        budget -= 51
        ssdMoney = 51
    else:
        ssdMoney = round((budget * .051), 2)
    
    budget = cleanBudget(budget, 800, 15000)

    return {
        "GPU": cleanBudget((budget * 0.306), 0, 5000),
        "CPU": cleanBudget((budget * 0.216), 0, 5000),
        "Windows Key": subtr,
        "RAM": cleanBudget((budget * 0.063)),
        "CASE": (caseMoney),
        "PSU": cleanBudget((budget * .083)),
        "SSD": ssdMoney,
        "HDD": cleanBudget((budget * .046)),
        "Motherboard": cleanBudget((budget * .085)),
        "CPU Cooler": cleanBudget((budget * .029)),
        "Wifi Adapter": cleanBudget((budget * .025)),
        "Peripherals": cleanBudget((budget * .046))
    }

def gatherPartData(part):
    path = os.path.join('./data/', part + '.csv')
    df = pd.read_csv(path).dropna()
    pc_parts[part] = df[df.Price != -1]
    print(pc_parts[part])
    
def findPartsWithinBudget(part, budget, preferredBrand, ssdStorageSpace, hddStorageSpace):
    part_data = pc_parts[part]

    if preferredBrand:
        part_data = part_data[part_data["Name"] in preferredBrand]
    if ssdStorageSpace:
        part_data = part_data[part_data["Capacity"].astype(int) >= ssdStorageSpace]
    if hddStorageSpace:
        part_data = part_data[part_data["Capacity"].astype(int) >= hddStorageSpace]
    
    part_data = part_data[part_data["Price"] <= budget]
    return part_data.iloc[0]['Name']

def buildPc(budget, cpu, ssdStorageSpace, hddStorageSpace):
    return {
        "GPU": findPartsWithinBudget("GPU", budget["GPU"], None, None, None),
        "CPU": findPartsWithinBudget("CPU", budget["CPU"], cpu, None, None),
        "RAM": findPartsWithinBudget("RAM", budget["RAM"], None, None, None),
        "CASE": findPartsWithinBudget("CASE", budget["CASE"], None, None, None),
        #"PSU": findPartsWithinBudget("power-supply", budget["PSU"]),
        "SSD": findPartsWithinBudget("SSD", budget["SSD"], None, ssdStorageSpace, None),
        "HDD": findPartsWithinBudget("HDD", budget["HDD"], None, None, hddStorageSpace),
        #"Motherboard": findPartsWithinBudget("motherboard", budget["Motherboard"]),
        #"CPU Cooler": findPartsWithinBudget("cpu-cooler", budget["CPU Cooler"]),
    }

for part in parts:
    print("Gathering part data for", part)
    gatherPartData(part)