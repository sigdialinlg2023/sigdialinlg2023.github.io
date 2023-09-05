#!/usr/bin/env python3

import pandas as pd

# Load the TSV data
tsv_data = pd.read_csv("scripts/inlg_genchalpapers.tsv", sep="\t")

# Define the conference name
conference = "inlg"

# Calculate the order within a session
tsv_data["order"] = tsv_data.groupby("session_uid").cumcount()

# Prepare the data for appending to the CSV
appended_data = {
    "conference": conference,
    "original_id": tsv_data["paper id"],
    "UID": "inlg" + tsv_data["paper id"].astype(str),
    "title": tsv_data["paper name"],
    "authors": tsv_data["authors"],
    "order": tsv_data["order"],
    "session": tsv_data["session_uid"],
    "paper_id": tsv_data["paper id"],
    "abstract": "",
    "paper": "",
    "notes": "",
}

# Load the CSV data
csv_data = pd.read_csv("sitedata/papers.csv")

# Append the new data to the CSV
appended_df = pd.DataFrame(appended_data)

result_df = pd.concat([csv_data, appended_df])

# Save the updated CSV
result_df.to_csv("sitedata/papers.csv", index=False)
