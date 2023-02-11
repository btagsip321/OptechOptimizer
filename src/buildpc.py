import pandas as pd
import json
import pdb
parts = ['CPU','GPU','HDD','RAM','SSD']
pc_parts = {'CPU':None, 'GPU':None, 'HDD':None, 'RAM':None, 'SSD':None}
def buildBudget(budget, windows):
    subtr = (100 if windows else 10)
    budget -= subtr
    
    return {
        "GPU": round((budget * 0.306), 2),
        "CPU": round((budget * 0.216), 2),
        "Windows Key": subtr,
        "RAM": round((budget * 0.063), 2),
        "Case": round((budget * .05), 2),
        "PSU": round((budget * .083), 2),
        "SSD": round((budget * .051), 2),
        "HDD": round((budget * .046), 2),
        "Motherboard": round((budget * .085), 2),
        "CPU Cooler": round((budget * .029), 2),
        "Wifi Adapter": round((budget * .025), 2),
        "Peripherals": round((budget * .046), 2)
    }
def gatherPartData(part):
    path = 'C:\\Code\\OptechOptimizer\\rendered_data\\CPU_UserBenchmarks.csv'
    df = pd.read_csv(path).dropna()
    df_filtered = df[pd.to_numeric(df['Price'], errors='coerce').notnull()]
    pc_parts[part] = df_filtered

def findPartsWithinBudget(part, budget):
    topPrice = int(budget)
    part_data = pc_parts[part]
    part_data["Price"] = pd.to_numeric(part_data['Price'])
    part_data = part_data.sort_values(by=['Rank'], ascending=True)
    updated_part_data = part_data[part_data["Price"] <= budget]
    return updated_part_data.iloc[0]['Brand'] + " " + updated_part_data.iloc[0]['Model'] + " Part Number: " + updated_part_data.iloc[0]['Part Number']

def buildPc(budget):
    return {
        "GPU": findPartsWithinBudget("video-card", budget["GPU"]),
        "CPU": findPartsWithinBudget("cpu", budget["CPU"]),
        "RAM": findPartsWithinBudget("memory", budget["RAM"]),
        "Case": findPartsWithinBudget("case", budget["Case"]),
        "PSU": findPartsWithinBudget("power-supply", budget["PSU"]),
        "SSD": findPartsWithinBudget("external-hard-drive", budget["SSD"]),
        "Motherboard": findPartsWithinBudget("motherboard", budget["Motherboard"]),
        "CPU Cooler": findPartsWithinBudget("cpu-cooler", budget["CPU Cooler"]),
    }
gatherPartData('CPU')
print(findPartsWithinBudget('CPU', 500))