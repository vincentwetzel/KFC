from collections import defaultdict

import pandas

original_file_name = "CD4 Republicans.csv"
print("Creating DataFrame...")
df_full_data_set = pandas.read_csv(original_file_name, encoding="utf-8",
                                   dtype={"Phone 2": object})
print("DataFrame created.")

df_by_leg_dist = defaultdict(pandas.DataFrame)
print("Splitting DataFrame into smaller DataFrames...")
for row_idx, voter in df_full_data_set.iterrows():
    df_by_leg_dist[voter["LegDistrict"]] = df_by_leg_dist[voter["LegDistrict"]].append(voter)
    if row_idx % 1000 == 0:
        print("Working on item: " + str(row_idx))
print("DataFrame splitting complete.")

print("Writing to output files...")
for leg_dist, df in df_by_leg_dist.items():
    print("Working on leg district: " + str(leg_dist))
    df = df.applymap(lambda x: x.encode('unicode_escape').
                     decode('utf-8') if isinstance(x, str) else x)
    df.to_excel(original_file_name.split(".")[0] + "_LD" + str(leg_dist) + ".xlsx", index=False, encoding="utf-8")
print("Done!")
