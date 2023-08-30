#!/usr/bin/env python3

import os
import pandas as pd

# Define a list to store data from each paper
data = []

# Define the top-level folder containing subfolders
top_folder = "/data/Uni/ufal/sigdial/final"  # Replace with the actual path

# Iterate through the subfolders
for folder_name in os.listdir(top_folder):
    folder_path = os.path.join(top_folder, folder_name)

    # Check if the item is a directory
    if os.path.isdir(folder_path):
        # Extract paper_id from the folder name
        paper_id = folder_name

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

            # Append the data to the list
            data.append([paper_id, paper_abstract])

# Create a Pandas DataFrame
df = pd.DataFrame(data, columns=["paper_id", "paper_abstract"])


# Load the existing CSV file into a DataFrame
existing_df = pd.read_csv("sitedata/papers.csv")

# Merge the existing DataFrame with the 'df' DataFrame on 'original_id' and 'paper_id'
merged_df = existing_df.merge(df, left_on="original_id", right_on="paper_id", how="left")

# Rename the new column as needed (e.g., 'paper_abstract')
merged_df.rename(columns={"paper_abstract": "abstract"}, inplace=True)

# Save the updated DataFrame back to the CSV file
merged_df.to_csv("sitedata/papers.csv", index=False)
