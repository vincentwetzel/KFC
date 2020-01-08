import os
from collections import defaultdict

precincts_with_dups = list()
with open("../archive_data/precincts_with_dups.txt") as pfile:
    precincts_with_dups = pfile.readlines()
for idx, prec in enumerate(precincts_with_dups):
    precincts_with_dups[idx] = precincts_with_dups[idx].strip()

leg_dist_with_dups = list()
with open("../archive_data/leg_dist_with_dups.txt") as lfile:
    leg_dist_with_dups = lfile.readlines()
for idx, prec in enumerate(leg_dist_with_dups):
    leg_dist_with_dups[idx] = leg_dist_with_dups[idx].strip()

leg_dist_clean = list()
for dist in leg_dist_with_dups:
    if dist not in leg_dist_clean:
        leg_dist_clean.append(dist)

master_dict = defaultdict(list)
for idx, leg_dist in enumerate(leg_dist_with_dups):
    master_dict[leg_dist].append(precincts_with_dups[idx])

counter = 0
for idx, leg_dist in enumerate(leg_dist_clean):
    os.mkdir(os.path.join(os.path.realpath(""), leg_dist))
    for idx2, precinct in enumerate(master_dict[leg_dist]):
        print("working...")
        try:
            os.mkdir(os.path.join(os.path.join(os.path.realpath(""), leg_dist),
                                  master_dict[leg_dist][idx2]))
        except FileExistsError:
            pass