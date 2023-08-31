#!/usr/bin/env python3

"""
Parses the following document https://docs.google.com/document/d/1a2PrGH_PE8idJpMsZhO8qnYJXy8vxgavW4t7BvaZ3OM/edit exported as html and creates a TSV file with papers, authors, and sessions.

The TSV can be further mapped to papers.csv using `annotate_papers_with_sessions.py`
"""

from bs4 import BeautifulSoup
import re

# path to the exported GDoc
with open("scripts/SigdialProgram.html") as f:
    html = f.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Initialize a list to store the extracted data
data = []

# Find all tables in the HTML
tables = soup.find_all("table")

tsv_headers = f"paper_id\tpaper_title\tauthors\tsession\torder"
data.append(tsv_headers)

# Iterate through each table
for table in tables:
    # Find all rows in the table
    rows = table.find_all("tr")

    paper_order = 0

    # Iterate through each row
    for row in rows:
        # Find all cells in the row
        cells = row.find_all("td")

        # Check if there are at least three cells (paper id, title and authors)
        if len(cells) >= 3:
            # Extract the paper title and authors
            paper_id = cells[0].text.strip()
            paper_title = cells[1].text.strip()
            authors = cells[2].text.strip()

            # find if the paper has some notes such as "(VIRTUAL)" or "(DEMO)" in the title and if so, remove it
            paper_title = re.sub(r"\s+\(\w+\)$", "", paper_title, flags=re.IGNORECASE)

            # also cut id to first three characters
            paper_id = paper_id.strip()[:3]

            # Extract the session information from the previous <p> tag
            session_info = row.find_previous("p", class_="c21").text.strip()

            # Combine the extracted information into a single string
            tsv_line = f"{paper_id}\t{paper_title}\t{authors}\t{session_info}\t{paper_order}"

            # Append the line to the data list
            data.append(tsv_line)

            paper_order += 1
        else:
            print(f"Skipping row: {row}")

# Define the output TSv file name
output_file = "scripts/sigdial_sessions_exported.tsv"

# Write the data to a TSv file
with open(output_file, "w", newline="", encoding="utf-8") as tsvfile:
    for line in data:
        tsvfile.write(line + "\n")

print(f'TSV file "{output_file}" has been created.')
