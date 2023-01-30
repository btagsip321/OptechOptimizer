from pcpartpicker import API
import pandas as pd
import json
import pdb

partpickerAPI = API()
raw_data = json.loads(partpickerAPI.retrieve_all().to_json())
pc_parts = {}

for part, info in raw_data.items():
    print(part)
    pc_parts[part] = pd.DataFrame(raw_data[part])
    pc_parts[part]['price'] = pc_parts[part]['price'].apply(lambda x: float(x[1]))

cpu_data = pc_parts["cpu"].sort_values(by=['price'], ascending=False)
cpu_data = cpu_data[cpu_data["price"].between(0, 200)]
print(cpu_data.iloc[0])