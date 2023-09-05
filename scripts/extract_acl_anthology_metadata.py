#!/usr/bin/env python3

import os
import pandas as pd
import shutil
import re

# Define a list to store data from each paper
data = []

# Define the top-level folder containing subfolders
conference = "sigdial"
top_folder = f"/data/Uni/events/2023_sigdial/anthology/{conference}"  # Replace with the actual path

# Iterate through the subfolders
for folder_name in os.listdir(top_folder):
    folder_path = os.path.join(top_folder, folder_name)

    # Check if the item is a directory
    if os.path.isdir(folder_path):
        # Extract paper_id from the folder name
        paper_id = folder_name

        paper_abstract = None
        paper_path = None

        # Construct the path to the metadata file
        txt_metadata_file = os.path.join(folder_path, f"{paper_id}_metadata.txt")
        html_metadata_file = os.path.join(folder_path, f"{paper_id}.html")

        # Check if the metadata file exists
        if os.path.isfile(txt_metadata_file):
            # Read the metadata from the file
            with open(txt_metadata_file, "r", encoding="utf-8") as file:
                metadata = file.read()

            # Extract the abstract from the metadata
            abstract_start = metadata.find("Abstract#==#") + len("Abstract#==#")
            abstract_end = metadata.find("Author{1}{Firstname}#=%=#")
            paper_abstract = metadata[abstract_start:abstract_end].strip()

            # Remove all newlines from the abstract
            paper_abstract = paper_abstract.replace("\n", " ")

        elif os.path.isfile(html_metadata_file):
            # Read the metadata from the file
            with open(html_metadata_file, "r", encoding="utf-8") as file:
                html_text = file.read()

            # Define a regular expression pattern to match the abstract
            abstract_pattern = r"<h3>Abstract<\/h3>\s*<blockquote>\s*<p>(.*?)<\/p>\s*<\/blockquote>"

            # Yes, we're parsing HTML with regexes and we're not ashamed of it
            match = re.search(abstract_pattern, html_text, re.DOTALL)

            if match:
                paper_abstract = match.group(1).strip().replace("\n", " ")
            else:
                breakpoint()

        # Construct the path to the metadata file

        if conference == "inlg":
            paper_file = os.path.join(folder_path, f"{paper_id}_Paper.pdf")
        else:
            paper_file = os.path.join(folder_path, f"{paper_id}.pdf")

        # Check if the paper file exists
        if os.path.isfile(paper_file):
            # copy and rename the paper file to "{paper_id}_Paper.pdf"
            shutil.copy(paper_file, f"static/papers/{conference}/{paper_id}_Paper.pdf")

            paper_path = f"static/papers/{conference}/{paper_id}_Paper.pdf"

        # Append the data to the list
        data.append([paper_id, paper_abstract, paper_path])

# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=["paper_id", "abstract", "paper"])

# prepend the conference name to the paper_id for each item in the column
df["paper_id"] = df["paper_id"].apply(lambda x: f"{conference}{x}")

# Load the existing CSV file into a DataFrame
existing_df = pd.read_csv("sitedata/papers.csv")

# # drop the existing columns "paper_id", "abstract", "paper" if they exist
# existing_df.drop(columns=["paper_id", "abstract", "paper"], inplace=True, errors="ignore")
# Merge the existing DataFrame with the 'df' DataFrame on 'original_id' and 'paper_id', overwrite existing columns if the new are non-empty
merged_df = existing_df.merge(df, left_on="UID", right_on="paper_id", how="left")

merged_df["abstract_x"] = merged_df["abstract_x"].fillna(merged_df["abstract_y"])
merged_df["paper_x"] = merged_df["paper_x"].fillna(merged_df["paper_y"])

# Drop the unnecessary columns
merged_df = merged_df.drop(columns=["abstract_y", "paper_y", "paper_id_x", "paper_id_y"])

# Rename the columns if needed
merged_df = merged_df.rename(columns={"abstract_x": "abstract", "paper_x": "paper"})
# Save the updated DataFrame back to the CSV file
breakpoint()

merged_df.to_csv("sitedata/papers.csv", index=False)
