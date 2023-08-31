#!/usr/bin/env python3

import os
import pandas as pd
import shutil

# Define a list to store data from each paper
data = []

# Define the top-level folder containing subfolders
conference = "inlg"
top_folder = f"/data/Uni/ufal/sigdial/anthology/{conference}"  # Replace with the actual path

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
        metadata_file = os.path.join(folder_path, f"{paper_id}_metadata.txt")

        # Check if the metadata file exists
        if os.path.isfile(metadata_file):
            # Read the metadata from the file
            with open(metadata_file, "r", encoding="utf-8") as file:
                metadata = file.read()

            # Extract the abstract from the metadata
            abstract_start = metadata.find("Abstract#==#") + len("Abstract#==#")
            abstract_end = metadata.find("Author{1}{Firstname}#=%=#")
            paper_abstract = metadata[abstract_start:abstract_end].strip()

            # Remove all newlines from the abstract
            paper_abstract = paper_abstract.replace("\n", " ")

        # Construct the path to the metadata file
        paper_file = os.path.join(folder_path, f"{paper_id}_Paper.pdf")

        # Check if the paper file exists
        if os.path.isfile(paper_file):
            shutil.copy(paper_file, f"static/papers/{conference}")

            paper_path = f"static/papers/{conference}/{paper_id}_Paper.pdf"

        # Append the data to the list
        data.append([paper_id, paper_abstract, paper_path])

# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=["paper_id", "abstract", "paper"])


# Load the existing CSV file into a DataFrame
existing_df = pd.read_csv("sitedata/papers.csv")

# drop the existing columns "paper_id", "abstract", "paper" if they exist
existing_df.drop(columns=["paper_id", "abstract", "paper"], inplace=True, errors="ignore")

# Merge the existing DataFrame with the 'df' DataFrame on 'original_id' and 'paper_id'
merged_df = existing_df.merge(df, left_on="original_id", right_on="paper_id", how="left")

# Remove duplicate columns
merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]

# Rename the new column as needed (e.g., 'paper_abstract')
# merged_df.rename(columns={"paper_abstract": "abstract", "paper_name": "paper"}, inplace=True)

breakpoint()

# Save the updated DataFrame back to the CSV file
merged_df.to_csv("sitedata/papers.csv", index=False)
