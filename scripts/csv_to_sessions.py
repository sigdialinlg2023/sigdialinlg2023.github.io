#!/usr/bin/env python3

import csv
import argparse
import datetime
import pytz
import re
import json


def process_file(in_file, cal_file):

    sessions = {}
    counters = {}

    with open(in_file, "r", encoding="UTF-8") as fh:
        tz = pytz.timezone("Europe/Prague")
        reader = csv.reader(fh, delimiter=",", quotechar='"')
        current_date = None
        dts = set()
        locations = None
        for row in reader:
            try:
                dt = datetime.datetime.strptime(row[0], "%b-%d")
                current_date = datetime.datetime(year=2023, month=dt.month, day=dt.day).date()
                locations = row[1:]
                continue
            except ValueError:
                pass

            if not current_date:
                continue

            try:
                dt = datetime.datetime.strptime(row[0], "%H:%M")
                dt = tz.localize(dt.combine(current_date, dt.time()))
                dts.add(dt.isoformat())
                for sess, loc in zip(row[1:], locations):
                    if not sess:
                        continue
                    sess = re.sub(r"(long paper )?talks", "Oral Session", sess, flags=re.I)
                    sess = re.sub(r"posters", "Poster Session", sess, flags=re.I)
                    sess = re.sub(r"\([^)]*\)", "", sess)
                    # sess = re.sub(r'[0-9-]*', '', sess)
                    m = re.search(r' till ([0-9:]+)', sess)
                    if m:
                        endtime = tz.localize(dt.combine(current_date, datetime.datetime.strptime(m.group(1), "%H:%M").time())).isoformat()
                        sess = re.sub(r' till.*', '', sess)
                    else:
                        endtime = None
                    sess = sess.strip()
                    sess = sess[0].upper() + sess[1:]
                    sessid = sess.lower().replace(" ", "")
                    if sessid == "end":
                        continue
                    if sessid in sessions:
                        counters[sessid] = 1
                        sessions[sessid + "1"] = sessions[sessid]
                        sessions[sessid + "1"]["UID"] = sessid + "1"
                        sessions[sessid + "1"]["UID"] = sessid + "1"
                        if sessid not in ["lunch", "coffeebreak"]:
                            sessions[sessid + "1"]["title"] += " 1"
                        del sessions[sessid]
                    if sessid in counters:
                        counters[sessid] += 1
                        if sessid not in ["lunch", "coffeebreak"]:
                            sess = sess + " " + str(counters[sessid])
                        sessid = sessid + str(counters[sessid])
                    sessions[sessid] = {
                        "UID": sessid,
                        "title": sess,
                        "start": dt.isoformat(),
                        "room": loc,
                        "category": "time",
                    }
                    if endtime:
                        sessions[sessid]["end"] = endtime
            except ValueError:
                pass

    sessions = sorted(sessions.values(), key=lambda s: s["start"])
    dts = sorted(list(dts))

    for session in sessions:
        if "end" not in session:
            session["end"] = dts[dts.index(session["start"]) + 1]
        category = session["UID"]
        category = re.sub(r"[0-9]+$", "", category)
        category = re.sub(r"presentation", "oral", category)
        category = re.sub(r"(keynote|business|poster|oral).*", r"\1", category)
        category = re.sub(r"virtual", "sigdial", category)
        category = re.sub(r"(inlg)?genchal", "inlg", category)
        category = {
            "coffeebreak": "break",
            "lunch": "break",
            "sponsors": "business",
            "closing": "business",
            "opening": "business",
            "welcomereception": "social",
            "conferencedinner": "social",
            "birdsoffeather": "social",
            "panel": "keynote",
        }.get(category, category)
        session["calendarId"] = category

    with open(cal_file, "w", encoding="UTF-8") as fh:
        json.dump(sessions, fh, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--in-file", required=True, type=str, help="Input CSV")
    ap.add_argument("-c", "--cal-file", required=True, type=str, help="Output calendar JSON")

    args = ap.parse_args()
    process_file(args.in_file, args.cal_file)
