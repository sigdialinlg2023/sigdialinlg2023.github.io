#!/usr/bin/env python3

import csv
import argparse
import datetime
import pytz
import re
import json
import yaml


def process_file(in_file, cal_file, sessions_links_file):


    sessions_links = yaml.load(open(sessions_links_file).read(), Loader=yaml.SafeLoader)
    session2discord = sessions_links["session2discord"]

    sessions = {}
    counters = {}
    uniq_locations = set()

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
                    uniq_locations.add(loc)
                    if not sess:
                        continue
                    sess = re.sub(r"(long paper )?talks", "Oral Session", sess, flags=re.I)
                    sess = re.sub(r"posters", "Poster Session", sess, flags=re.I)
                    sess = re.sub(r"\([^)]*\)", "", sess)
                    sess = re.sub(r"[0-9]+-[0-9]+", "", sess)
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
    sessions_uids = [s["UID"] for s in sessions]
    assert len(set(sessions_uids)) == len(sessions_uids), f"{sessions_uids=} ARE NOT UNIQUE!"
    discord_sessions = sorted(session2discord.keys())
    assert all(s in sessions_uids for s in discord_sessions), f"{sessions_uids=} vs {discord_sessions=}"
    room2zoom = sessions_links["rooms2zoom"]
    rooms_for_zoom = sorted(room2zoom.keys())
    assert all(r in uniq_locations for r in rooms_for_zoom), f"{rooms_for_zoom=} vs {uniq_locations=}"


    dts = sorted(list(dts))

    for session in sessions:
        discord_url = session2discord.get(session["UID"])
        if discord_url is not None:
            session["discord"] = discord_url
            session["zoom"] = room2zoom.get(session["room"])

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
            "birds-of-feather": "discussion",
            "panel": "discussion",
            "welcomereception": "social",
            "conferencedinner": "social",
        }.get(category, category)
        session["calendarId"] = category

    with open(cal_file, "w", encoding="UTF-8") as fh:
        json.dump(sessions, fh, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--in-file", required=True, type=str, help="Input CSV")
    ap.add_argument("-c", "--cal-file", required=True, type=str, help="Output calendar JSON")
    ap.add_argument("-s", "--sessions_links_file", default="./sitedata/sessions_links.yml", help="File for managing links to Discord and Zoom links for each sessions")

    args = ap.parse_args()
    process_file(args.in_file, args.cal_file, args.sessions_links_file)
