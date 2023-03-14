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
    path = os.path.join('./old_data/', part + '_UserBenchmarks.csv')
    df = pd.read_csv(path).dropna()
    
    if(part == "SSD" or part == "HDD"):
        for(index, modelNo) in df["Model"].items():
            if("GB" in modelNo):
                place = modelNo.index("GB")
                threeBefore = place - 3
                if(modelNo[threeBefore:place].isdigit):
                    df.at[index, "SizeGB"] = modelNo[threeBefore:place]
            elif("TB" in modelNo):
                place = modelNo.index("TB")
                twoBefore = place - 2
                oneBefore = place - 1
                if(modelNo[twoBefore:place].isdigit):
                    df.at[index, "SizeGB"] = int(modelNo[twoBefore:place]) * 1000
                elif(modelNo[oneBefore:place].isdigit):
                    df.at[index, "SizeGB"] = int(modelNo[oneBefore:place]) * 1000
    pc_parts[part] = df[pd.to_numeric(df['Price'], errors='coerce').notnull()]


def findPartsWithinBudget(part, budget, preferredBrand, ssdStorageSpace, hddStorageSpace):
    part_data = pc_parts[part]

    if preferredBrand:
        part_data = part_data[part_data["Brand"] == preferredBrand]
    if ssdStorageSpace:
        part_data = part_data[part_data["SizeGB"].astype(int) >= ssdStorageSpace]
    if hddStorageSpace:
        part_data = part_data[part_data["SizeGB"].astype(int) >= hddStorageSpace]
    
    part_data["Price"] = pd.to_numeric(part_data['Price'])
    part_data = part_data.sort_values(by=['Rank'], ascending=True)
    updated_part_data = part_data[part_data["Price"] <= budget]
    return updated_part_data.iloc[0]['Brand'] + " " + updated_part_data.iloc[0]['Model'] + " Part Number: " + updated_part_data.iloc[0]['Part Number'] + " Price: " + str(updated_part_data.iloc[0]["Price"]) + " Buy Here: " + updated_part_data.iloc[0]["URL"]

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
    
