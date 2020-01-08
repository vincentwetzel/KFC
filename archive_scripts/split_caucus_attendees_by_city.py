import pandas as pd
import csv
from collections import defaultdict
from typing import List, DefaultDict

# Dump data into lists
print("Dumping data into lists...")
data_by_cities_dict = defaultdict(list)
df = pd.read_excel("CD4_2016_2018_Caucus_Attendees.xlsx", encoding="utf-8")
for idx, row_data in df.iterrows():
    city_name = row_data["City"]
    if row_data["2016 CA"] == 1 and pd.isnull(row_data["2018 CA"]):
        data_by_cities_dict[city_name + " 2016"].append(row_data)
    elif pd.isnull(row_data["2016 CA"]) and row_data["2018 CA"] == 1:
        data_by_cities_dict[city_name + " 2018"].append(row_data)
    elif row_data["2016 CA"] == 1 and row_data["2018 CA"] == 1:
        data_by_cities_dict[city_name + " 2016 and 2018"].append(row_data)
    else:
        print(row_data)
        raise Exception("This person didn't go to either 2016 or 2018 so why are the on this list???")

# Create new dataframes
print("Initial data compiled. Creating new dataframes...")
new_dataframes_list = list()
new_dataframes_city_names = list()
for city in data_by_cities_dict.keys():
    new_dataframes_list.append(pd.DataFrame(data_by_cities_dict[city]))
    new_dataframes_city_names.append(city)

print("Writing new dataframes to CSV...")
for idx, data_frame in enumerate(new_dataframes_list):
    data_frame.to_csv(str(new_dataframes_city_names[idx]) + " (" + str(len(data_frame)) + ").csv", index=False)

print("DONE!")
