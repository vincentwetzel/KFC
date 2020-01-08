import re

precincts_cities = list()

with open("all_precincts_by_abbrev.txt", "r") as f:
    for line in f.readlines():
        line = re.sub(r'\d+', '', line.strip())
        if line not in precincts_cities:
            precincts_cities.append(line)

for p in precincts_cities:
    print(p)
print(len(precincts_cities))