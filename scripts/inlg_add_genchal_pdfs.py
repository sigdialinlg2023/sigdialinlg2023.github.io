#!/usr/bin/env python3

import pandas as pd
import os

# Load the CSV data
csv_data = pd.read_csv("sitedata/papers.csv")

# for a file in papers.csv
# if there is a corresponding file in sitedata/papers/genchal/<paper_id>.pdf
# add the path to the `paper` column
for index, row in csv_data.iterrows():
    # if paper is from sigdial, skip
    if row["conference"] == "sigdial":
        continue
    paper_id = row["original_id"]
    pdf_path = f"static/papers/genchal/{paper_id}.pdf"
    # if the file exists, add the path to the `paper` column
    if os.path.isfile(pdf_path):
        csv_data.loc[index, "paper"] = pdf_path
        print(pdf_path)

# Save the updated CSV
csv_data.to_csv("sitedata/papers.csv", index=False)
