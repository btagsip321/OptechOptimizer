from pcpartpicker import API
import pandas as pd
import json
import pdb

api = API()
cpu_data = api.retrieve("cpu")
cpu_data_json = cpu_data.to_json()
cpu_dict = json.loads(cpu_data_json)
cpu_dict2 = cpu_dict['cpu']
cpu_df = pd.DataFrame(cpu_dict2)
cpu_df = cpu_df[['price', 'brand', 'model']]
bench = pd.read_csv("CPU_UserBenchmarks.csv")
bench = bench[['Brand', 'Model', 'Rank']]
#bench["UpdatedModel"] = bench["Brand"].astype(str) + " " + bench["Model"]
benchPrice = pd.merge(cpu_df, bench, how="inner", left_on="model", right_on="Model")
#benchPrice = benchPrice[benchPrice.price[1] != '0.00']
benchPrice = benchPrice[["price", "brand", "model", "Rank"]]
pdb.set_trace() 