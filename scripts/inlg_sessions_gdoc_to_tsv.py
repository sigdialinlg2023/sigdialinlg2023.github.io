#!/usr/bin/env python3

"""
Parses the tab of the following document https://docs.google.com/spreadsheets/d/1O-0oyN8gMkcXJ4dFoqs-V6QS6XNRmayF/edit#gid=1436618776 exported to CSV and creates a TSV file with papers, authors, and sessions.

Note that the CSV should have only lines with sessions (+header) and nothing else - I found it easier to do it manually than to code complex rules.

The TSV can be further mapped to papers.csv using `annotate_papers_with_sessions.py`
"""

import pandas as pd

# Read the CSV file into a Pandas DataFrame
df = pd.read_csv("scripts/INLGProgram.csv", delimiter=",")

# Create a new DataFrame with the following columns:
# paper_id, paper_title, authors, session, order
df_processed = pd.DataFrame(columns=["paper_title", "authors", "session_uid", "order"])

# Iterate over the rows in the DataFrame
for index, row in df.iterrows():
    # Get the session name and session UID
    session_name = row["session name"]
    session_uid = row["Session UID"]

    # Split the papers column into a list of paper titles and authors
    papers_all = row["papers"].split("\n")

    # remove empty lines and strip the rest
    papers_all = [p.strip() for p in papers_all if p]

    # papers are every odd item, authors every even item
    papers = papers_all[::2]
    authors = papers_all[1::2]

    for i, (paper, author) in enumerate(zip(papers, authors)):
        # Create a new row in the DataFrame using pandas.concat
        df_processed = pd.concat(
            [
                df_processed,
                pd.DataFrame(
                    {
                        "paper_title": [paper],
                        "authors": [author],
                        "session_uid": [session_uid],
                        "order": [i],
                    }
                ),
            ]
        )

# Write the processed DataFrame to a TSV file
df_processed.to_csv("scripts/inlg_sessions_exported.tsv", sep="\t", index=False)
