import pandas as pd
import json
import pdb
import os

parts = ['CPU','GPU','HDD','RAM','SSD', 'CASE']
pc_parts = {'CPU':None, 'GPU':None, 'HDD':None, 'RAM':None, 'SSD':None, 'CASE':None}

def buildBudget(budget, windows):
    subtr = (100 if windows else 10)
    budget -= subtr
    if((budget * .05) < 45):
        budget -= 45
        caseMoney = round((45), 2)
    else:
        caseMoney = round((budget * .05), 2)
    if((budget * .051 < 51)):
        budget -= 51
        ssdMoney = 51
    else:
        ssdMoney = round((budget * .051), 2)
    
    return {
        "GPU": round((budget * 0.306), 2),
        "CPU": round((budget * 0.216), 2),
        "Windows Key": subtr,
        "RAM": round((budget * 0.063), 2),
        "CASE": (caseMoney),
        "PSU": round((budget * .083), 2),
        "SSD": ssdMoney,
        "HDD": round((budget * .046), 2),
        "Motherboard": round((budget * .085), 2),
        "CPU Cooler": round((budget * .029), 2),
        "Wifi Adapter": round((budget * .025), 2),
        "Peripherals": round((budget * .046), 2)
    }


def gatherPartData(part):
    path = os.path.join('./rendered_data/', part + '_UserBenchmarks.csv')
    df = pd.read_csv(path).dropna()
    pc_parts[part] = df[pd.to_numeric(df['Price'], errors='coerce').notnull()]

def findPartsWithinBudget(part, budget, preferredBrand):
    part_data = pc_parts[part]
    if preferredBrand:
        part_data = part_data[part_data["Brand"] == preferredBrand]

    part_data["Price"] = pd.to_numeric(part_data['Price'])
    part_data = part_data.sort_values(by=['Rank'], ascending=True)
    updated_part_data = part_data[part_data["Price"] <= budget]
    return updated_part_data.iloc[0]['Brand'] + " " + updated_part_data.iloc[0]['Model'] + " Part Number: " + updated_part_data.iloc[0]['Part Number']

def buildPc(budget, cpu, gpu):
    return {
        "GPU": findPartsWithinBudget("GPU", budget["GPU"], gpu),
        "CPU": findPartsWithinBudget("CPU", budget["CPU"], cpu),
        "RAM": findPartsWithinBudget("RAM", budget["RAM"], None),
        "CASE": findPartsWithinBudget("CASE", budget["CASE"], None),
        #"PSU": findPartsWithinBudget("power-supply", budget["PSU"]),
        "SSD": findPartsWithinBudget("SSD", budget["SSD"], None),
        "HDD": findPartsWithinBudget("HDD", budget["HDD"], None),
        #"Motherboard": findPartsWithinBudget("motherboard", budget["Motherboard"]),
        #"CPU Cooler": findPartsWithinBudget("cpu-cooler", budget["CPU Cooler"]),
    }

for part in parts:
    print("Gathering part data for", part)
    gatherPartData(part)

    
