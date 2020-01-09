#!/usr/bin/python3

import os
import re
from collections import defaultdict
from collections import OrderedDict
from typing import List
import pathlib

import pandas
from win32com.client import Dispatch

input_files_list: dict = {
    "CD4 Republicans_LD22.xlsx": "CD4 Voters_LD22.xlsx",
    "CD4 Republicans_LD25.xlsx": "CD4 Voters_LD25.xlsx",
    "CD4 Republicans_LD26.xlsx": "CD4 Voters_LD26.xlsx",
    "CD4 Republicans_LD30.xlsx": "CD4 Voters_LD30.xlsx",
    "CD4 Republicans_LD31.xlsx": "CD4 Voters_LD31.xlsx",
    "CD4 Republicans_LD32.xlsx": "CD4 Voters_LD32.xlsx",
    "CD4 Republicans_LD33.xlsx": "CD4 Voters_LD33.xlsx",
    "CD4 Republicans_LD34.xlsx": "CD4 Voters_LD34.xlsx",
    "CD4 Republicans_LD35.xlsx": "CD4 Voters_LD35.xlsx",
    "CD4 Republicans_LD36.xlsx": "CD4 Voters_LD36.xlsx",
    "CD4 Republicans_LD37.xlsx": "CD4 Voters_LD37.xlsx",
    "CD4 Republicans_LD38.xlsx": "CD4 Voters_LD38.xlsx",
    "CD4 Republicans_LD39.xlsx": "CD4 Voters_LD39.xlsx",
    "CD4 Republicans_LD40.xlsx": "CD4 Voters_LD40.xlsx",
    "CD4 Republicans_LD41.xlsx": "CD4 Voters_LD41.xlsx",
    "CD4 Republicans_LD42.xlsx": "CD4 Voters_LD42.xlsx",
    "CD4 Republicans_LD43.xlsx": "CD4 Voters_LD43.xlsx",
    "CD4 Republicans_LD44.xlsx": "CD4 Voters_LD44.xlsx",
    "CD4 Republicans_LD45.xlsx": "CD4 Voters_LD45.xlsx",
    "CD4 Republicans_LD46.xlsx": "CD4 Voters_LD46.xlsx",
    "CD4 Republicans_LD47.xlsx": "CD4 Voters_LD47.xlsx",
    "CD4 Republicans_LD50.xlsx": "CD4 Voters_LD50.xlsx",
    "CD4 Republicans_LD51.xlsx": "CD4 Voters_LD51.xlsx",
    "CD4 Republicans_LD52.xlsx": "CD4 Voters_LD52.xlsx"
}
for gop_file, all_generic_voter_file in input_files_list.items():
    print("Loading dataframes...")
    # Init dataframes
    all_gop_voters_df = pandas.read_excel(gop_file, encoding="utf-8")

    # Split GOP Leg District into precincts dict
    gop_by_precinct_df_dict = defaultdict(pandas.DataFrame)
    for row_idx, gop_precinct_voter in all_gop_voters_df.iterrows():
        gop_by_precinct_df_dict[gop_precinct_voter["Precinct"].split(":")[0]] = gop_by_precinct_df_dict[
            gop_precinct_voter["Precinct"].split(":")[0]].append(gop_precinct_voter)

    # Split Generic Leg Districts into precincts dict
    all_generic_voters_file_df = pandas.read_excel(all_generic_voter_file, encoding="utf-8")
    all_voters_by_precinct_df_dict = defaultdict(pandas.DataFrame)
    for row_idx, generic_voter in all_generic_voters_file_df.iterrows():
        all_voters_by_precinct_df_dict[generic_voter["Precinct"].split(":")[0]] = all_voters_by_precinct_df_dict[
            generic_voter["Precinct"].split(":")[0]].append(generic_voter)

    print("Dataframes loaded for Leg District " + gop_file.split(".")[0].split("CD4 Republicans_LD")[1])

    processed_count = 1
    success_count = 0
    failed_count = 0
    is_found = False
    curr_leg_dist = None

    fname_lname_addr_tup_list = list()
    for tup_idx, voter in all_generic_voters_file_df.iterrows():
        fname_lname_addr_tup_list.append((voter["First Name"], voter["Last Name"], voter["Address"]))

    for precinct, data_frame in gop_by_precinct_df_dict.items():
        destination_directory_str = os.path.realpath(
            os.path.join("structure/Leg District " + str(
                gop_file.split(".")[0].split("CD4 Republicans_LD")[1]) + "/" + precinct))
        if os.path.isfile(os.path.join(os.path.abspath(destination_directory_str), precinct + ".xlsx")):
            print("Precinct " + precinct + " has already been generated. Continuing.")
            continue
        print("Creating list of dataframes for precinct: " + precinct)
        list_of_output_data_frames_for_precinct: List[pandas.DataFrame] = list()
        for curr_gop_df_row_idx, gop_precinct_voter in data_frame.iterrows():
            is_found = False
            processed_count += 1
            for curr_all_voter_df_row_idx, cur_fname_lname_addr_tup in enumerate(fname_lname_addr_tup_list):
                if cur_fname_lname_addr_tup[0] == gop_precinct_voter[
                    "First Name"] and cur_fname_lname_addr_tup[1] == gop_precinct_voter[
                    "Last Name"] and cur_fname_lname_addr_tup[2] == gop_precinct_voter["Address"]:
                    curr_leg_dist = int(gop_precinct_voter["LegDistrict"])
                    gop_precinct_voter["Precinct"] = gop_precinct_voter["Precinct"].split(":")[0]
                    gop_precinct_voter["Age"] = all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Age"]
                    gop_precinct_voter["Phone"] = all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Phone"]
                    gop_precinct_voter["Phone2"] = all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Phone 2"]
                    gop_precinct_voter["Primary2014"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Primary 2014"]) else ""
                    gop_precinct_voter["Primary2016"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Primary 2016"]) else ""
                    gop_precinct_voter["Primary2018"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "Primary 2018"]) else ""
                    gop_precinct_voter["General2014"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "General 2014"]) else ""
                    gop_precinct_voter["General2016"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "General 2016"]) else ""
                    gop_precinct_voter["General2018"] = 1 if not pandas.isnull(
                        all_generic_voters_file_df.at[curr_all_voter_df_row_idx, "General 2018"]) else ""
                    gop_precinct_voter["StreetNumber"] = re.search(r"^[0-9]+", gop_precinct_voter["Address"]).group(
                        0).strip()
                    gop_precinct_voter["StreetName"] = re.search(r"(?<=[0-9 ])[a-zA-Z].+?(?=#|Apt|Unit|$)",
                                                                 gop_precinct_voter["Address"]).group(0).strip()
                    if re.search(r"Apt [0-9]+|Apt\. [0-9]+|\#[0-9]+|Unit [0-9]+",
                                 gop_precinct_voter["Address"]) is not None:
                        gop_precinct_voter["Unit"] = re.search(r"Apt [0-9]+|Apt\. [0-9]+|\#[0-9]+|Unit [0-9]+",
                                                               gop_precinct_voter["Address"]).group(0).strip()
                    else:
                        gop_precinct_voter["Unit"] = ""
                    success_count += 1
                    is_found = True
                    break

            if not is_found:
                print(
                    "Could not find: " + str(gop_precinct_voter["First Name"]) + " " + str(
                        gop_precinct_voter["Last Name"]))
                failed_count += 1
            list_of_output_data_frames_for_precinct.append(gop_precinct_voter)

        # Create output dataframes
        print("Writing precinct " + precinct + " to output file...")
        list_of_final_data_frames: List[pandas.DataFrame] = list()
        for df in list_of_output_data_frames_for_precinct:
            output_df = pandas.DataFrame(OrderedDict({"Response": "",
                                                      "StreetNumber": pandas.Series(df["StreetNumber"]),
                                                      "StreetName": pandas.Series(df["StreetName"]),
                                                      "Unit": pandas.Series(df["Unit"]),
                                                      "FirstName": pandas.Series(df["First Name"]),
                                                      "LastName": pandas.Series(df["Last Name"]),
                                                      "Age": pandas.Series(df["Age"]),
                                                      "City": pandas.Series(df["City"]),
                                                      "State": pandas.Series(df["State"]),
                                                      "Precinct": pandas.Series(df["Precinct"]),
                                                      "LegDistrict": pandas.Series(df["LegDistrict"]),
                                                      "SenateDistrict": pandas.Series(df["SenateDistrict"]),
                                                      "Phone": pandas.Series(df["Phone"]),
                                                      "Phone2": pandas.Series(df["Phone 2"]),
                                                      "Email": pandas.Series(df["Email"]),
                                                      "Primary2014": pandas.Series(df["Primary2014"]),
                                                      "Primary2016": pandas.Series(df["Primary2016"]),
                                                      "Primary2018": pandas.Series(df["Primary2018"]),
                                                      "General2014": pandas.Series(df["General2014"]),
                                                      "General2016": pandas.Series(df["General2016"]),
                                                      "General2018": pandas.Series(df["General2018"]),
                                                      "FullAddress": pandas.Series(df["Address"]),
                                                      }))
            list_of_final_data_frames.append(output_df)
        pathlib.Path(destination_directory_str).mkdir(parents=True, exist_ok=True)
        final_data_frame: pandas.DataFrame = pandas.concat(list_of_final_data_frames)
        final_data_frame.sort_values(by=["StreetName", "StreetNumber"], inplace=True)
        final_data_frame.to_excel(os.path.join(os.path.abspath(destination_directory_str), precinct + ".xlsx"),
                                  index=False)

        # Autosize the columns
        excel = Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(os.path.join(os.path.abspath(destination_directory_str), precinct + ".xlsx"))
        excel.Worksheets(1).Activate()
        excel.ActiveSheet.Columns.AutoFit()
        wb.Save()
        wb.Close()

print("Success Count for " + str(gop_file) + ": " + str(success_count))
print("Failed Count for " + str(gop_file) + ": " + str(failed_count))

print("Done!")
