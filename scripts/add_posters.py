#!/usr/bin/env python3

"""
Looks in static/posters and updates the `poster` column in `papers.csv`.
"""

import pandas as pd
import re
import sys
import os


def normalize_posters(folder, paper_id):
    # find all the papers that could be related to this paper
    # that could be "[p|P]aper.*<paper_id>\D.*.pdf" or "<paper_id>\D.*.pdf"
    # e.g. "paper 123.pdf", "Paper 123.pdf", "123.pdf", "123 (2).pdf", "123 (3).pdf"
    # but not "1234.pdf"

    # find all the files in the folder
    files = os.listdir(folder)

    # delete any non-pdf files
    files_to_delete = [f for f in files if not f.endswith(".pdf")]
    for f in files_to_delete:
        os.remove(f"{folder}/{f}")

    # filter out the files that don't match the pattern
    files = [f for f in files if re.search(r"(\D|^)" + paper_id + r"[\. \(]" + ".*pdf", f)]
    if files:
        print(paper_id, files)

    # if there are no files, return
    if len(files) == 0:
        return

    # if there is only one file, rename it to "paper_id.pdf"
    if len(files) == 1:
        os.rename(f"{folder}/{files[0]}", f"{folder}/{paper_id}.pdf")
        return

    # if there are multiple files, keep the one with the latest modification date and rename it to "paper_id.pdf", and delete the others
    if len(files) > 1:
        # get the modification time for each file
        mod_times = [os.path.getmtime(f"{folder}/{f}") for f in files]
        # get the index of the file with the latest modification time
        latest_file_index = mod_times.index(max(mod_times))
        # rename the file with the latest modification time to "paper_id.pdf"
        os.rename(f"{folder}/{files[latest_file_index]}", f"{folder}/{paper_id}.pdf")
        # delete the other files
        for i, f in enumerate(files):
            if i != latest_file_index:
                os.remove(f"{folder}/{f}")
        return


if __name__ == "__main__":
    conference = sys.argv[1]

    if conference == "sigdial":
        subfolder = "SIGDIAL2023"
    elif conference == "inlg":
        subfolder = "INLG2023"

    # Read the CSV file into a DataFrame
    df_csv = pd.read_csv("sitedata/papers.csv")

    if not os.path.exists(f"static/posters/thumbnails"):
        os.makedirs(f"static/posters/thumbnails")

    if not "poster" in df_csv:
        df_csv["poster"] = ""
    # if not "full_video" in df_csv:
    #     df_csv["full_video"] = ""

    # look into the static/posters folder and if there is a "<paper_id>.pdf" file, add it to the `poster` column, and if there is a "<paper_id>.mp4" file, add it to the `full_video` column
    for i, row in df_csv.iterrows():
        if row["conference"] != conference:
            continue

        paper_id = row["original_id"]
        paper_uid = row["UID"]

        normalize_posters(f"static/posters/{subfolder}/", paper_id)

        poster_path = f"static/posters/{subfolder}/{paper_id}.pdf"
        # video_path = f"static/posters/{subfolder}/{paper_id}.mp4"

        if os.path.exists(poster_path):
            df_csv.loc[i, "poster"] = f"static/posters/{subfolder}/{paper_id}.pdf"
            # create a thumbnail for the poster
            os.system(f"convert -thumbnail 200x200 {poster_path}[0] static/posters/thumbnails/{paper_uid}.png")
        # if os.path.exists(video_path):
        #     df_csv.loc[i, "full_video"] = f"static/videos/{subfolder}/{paper_id}.mp4"
        #     print(f"Found video for {paper_id}")


# Save the updated DataFrame to a new CSV file
df_csv.to_csv("sitedata/papers.csv", index=False)

print("papers.csv has been updated.")
