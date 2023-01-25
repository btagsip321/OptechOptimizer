from pcpartpicker import API
import pandas as pd
import json

partpickerAPI = API()
pc_parts = {}

for part, info in json.loads(partpickerAPI.retrieve_all().to_json()).items():
    pc_parts[part] = pd.DataFrame(info)
    pc_parts[part]['price'] = pc_parts[part]['price'].apply(lambda x: float(x[1]))

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

def findPartsWithinBudget(part, budget):
    part_data = pc_parts[part]
    return part_data[part_data["price"].between(0, 200)]

def buildPc(budget):
    return {
        #"GPU": findPartsWithinBudget("gpu", budget["gpu"]),
        "CPU": findPartsWithinBudget("cpu", budget["cpu"]),
    }