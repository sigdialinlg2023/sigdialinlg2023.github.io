#!/usr/bin/env python3


"""
Open sitedata/papers.csv and for the rows with following `UID` add a note "(Best Paper Nominee)" to the `notes` column:
"""

import pandas as pd
import re
import sys
import os


ids = [
    "sigdial19",
    "sigdial34",
    "sigdial50",
    "sigdial97",
    "inlg12",
    "inlg24",
    "inlg47",
    "inlg24",
    "inlg56",
    "inlg58",
    "inlg79",
    "inlg82",
]

if __name__ == "__main__":
    papers = pd.read_csv(f"sitedata/papers.csv")

    for i, row in papers.iterrows():
        if row["UID"] in ids:
            print(row["UID"])
            prev = (papers.loc[i, "notes"] + ", ") if type(papers.loc[i, "notes"]) is str else ""
            papers.loc[i, "notes"] = prev + "(Best Paper Nominee)"

    papers.to_csv(f"sitedata/papers.csv", index=False)
