"""
This script is to take Romney's 2018 SLCO results and eliminate all non-CD4 information.
"""

# Init CD4 precincts
CD4_SLCO_precincts = list()
with open("all_CD4_SLCO_precincts_by_abbrev.txt", 'r') as CD4_SLCO_precincts_file:
    CD4_SLCO_precincts = [line.strip for line in CD4_SLCO_precincts_file.readlines()]

print("Done!")
