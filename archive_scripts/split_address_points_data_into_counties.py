import csv
from collections import defaultdict
from typing import List, DefaultDict

import pandas as pd

# Init FIPS codes
counties_by_FIPS_code = dict()
reader = csv.reader(open("address_points_by_county/County_FIPS_codes.csv", 'r'))
column_names = next(reader, None)
for row_data in reader:
    k, v = row_data
    counties_by_FIPS_code[int(k.strip())] = v.strip()

# Dump data into lists
data_by_counties_dict = defaultdict(list)
df = pd.read_csv("../archive_data/Utah_Address_Points.csv", encoding="utf-8", dtype={"AddNum": object, "ParcelID": object})
for idx, row_data in df.iterrows():
    county_id = row_data["CountyID"]
    data_by_counties_dict[county_id].append(row_data)

# Init new dataframes
print("Initial data compiled. Creating new dataframes...")
new_dataframes_list = list()
new_dataframes_county_names = list()
for county_id_number in data_by_counties_dict.keys():
    new_dataframes_list.append(pd.DataFrame(data_by_counties_dict[county_id_number]))
    new_dataframes_county_names.append(counties_by_FIPS_code[county_id_number])

# Write new dataframes to CSV
print("Writing new dataframes to CSV...")
for idx, data_frame in enumerate(new_dataframes_list):
    data_frame.to_csv(str(new_dataframes_county_names[idx]) + ".csv", index=False)

print("DONE!")
