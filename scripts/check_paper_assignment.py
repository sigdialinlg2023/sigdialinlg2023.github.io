#!/usr/bin/env python3

import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv("sitedata/papers.csv")

# Print paper title + authors + conference for papers that are missing a session
print("Missing a session:")
print("-" * 80)
for i, row in df.iterrows():
    if pd.isnull(row["session"]):
        print(f"{row['title']} {row['authors']} ({row['conference']})")

print()
print()
print()
# Print papers that are missing an abstract
print("Missing an abstract:")
print("-" * 80)
for i, row in df.iterrows():
    if pd.isnull(row["abstract"]):
        print(f"{row['title']} ({row['conference']})")
