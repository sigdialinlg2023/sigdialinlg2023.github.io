# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
from datetime import datetime, timedelta
import glob
import json
import os
import re

import yaml
from flask import Flask, jsonify, redirect, render_template, send_from_directory
from flask_frozen import Freezer
from flaskext.markdown import Markdown

site_data = {}
by_uid = {}
by_date = {}


def get_minutes_per_paper(session_uid):
    if "poster" in session_uid:
        # posters last the whole session
        return 0
    elif "sigdial" in session_uid:
        return 20
    elif "genchal" in session_uid:
        # should be 10 for short papers but we have no good way to tell which paper is short in here
        return 15
    elif "inlg" in session_uid:
        return 25
    else:
        raise ValueError(f"Unknown session type: {session_uid}")


def main(site_data_path):
    global site_data, extra_files
    extra_files = ["Home.md"]
    # Load all for your sitedata one time.
    for f in glob.glob(site_data_path + "/*"):
        print(f)
        extra_files.append(f)
        name, typ = f.split("/")[-1].split(".")
        if typ == "json":
            site_data[name] = json.load(open(f))
        elif typ in {"csv", "tsv"}:
            site_data[name] = list(csv.DictReader(open(f)))
        elif typ == "yml":
            site_data[name] = yaml.load(open(f).read(), Loader=yaml.SafeLoader)

    id_to_session = {}
    # load main calendar
    for p in site_data["main_calendar"]:
        dt = datetime.fromisoformat(p["start"])
        if dt.strftime("%A") not in by_date:
            by_date[dt.strftime("%A")] = {"name": dt.strftime("%A"), "sessions": {}}
        p["contents"] = []
        p["name"] = p["title"]
        p["start_time"] = dt
        # links the calendar box to the session info
        p["location"] = f"#{p['UID']}"
        by_date[dt.strftime("%A")]["sessions"][p["UID"]] = p
        id_to_session[p["UID"]] = p

    # fill calendar with contents
    for typ in ["speakers", "papers"]:
        by_uid[typ] = {}
        if typ == "speakers":
            vals = site_data[typ]["speakers"]
            for p in vals:  # load session start times from calendar (avoid duplication)
                p["start"] = [s for s in site_data["main_calendar"] if s["UID"] == p["session"]][0]["start"]
        elif typ in ["workshops", "tutorials", "panels", "hackathons"]:
            vals = [format_workshop(workshop) for workshop in site_data[typ]]
        elif typ == "papers":
            vals = [format_paper(x) for x in site_data["papers"]]
        else:
            vals = site_data[typ]

        for p in vals:
            by_uid[typ][p["UID"]] = p

            sessions = p["session"].split("|") if p["session"] else []
            orders = p["order"].split("|") if "order" in p else [0] * len(sessions)
            start = p["start"] if "start" in p else None

            if not start:
                # paper mapped to session, calculate start relative to session start
                for session, order in zip(sessions, orders):
                    related_session = id_to_session[session]
                    session_start_datetime = datetime.fromisoformat(related_session["start"])

                    minutes_per_paper = get_minutes_per_paper(related_session["UID"])
                    # add order * X minutes to paper start time where X depends on the session type
                    start_time = session_start_datetime + timedelta(minutes=int(order) * minutes_per_paper)
                    p["start"] = start_time.isoformat()

            for session in sessions:
                dt = datetime.fromisoformat(p["start"])
                day = dt.strftime("%A")

                by_date[day]["sessions"][session]["contents"].append(p)

        for day in by_date.values():
            day["sessions"] = dict(sorted(day["sessions"].items(), key=lambda item: item[1]["start"]))
            for session in day["sessions"].values():
                session["contents"] = sorted(session["contents"], key=lambda item: item["start"])

    print("Data Successfully Loaded")
    return extra_files


# ------------- SERVER CODE -------------------->

app = Flask(__name__)
app.config.from_object(__name__)
freezer = Freezer(app)
markdown = Markdown(app, extensions=["tables"])


# MAIN PAGES


def _data():
    data = {}
    data["config"] = site_data["config"]
    return data


@app.route("/")
def index():
    return redirect("/index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(site_data_path, "favicon.ico")


# TOP LEVEL PAGES


@app.route("/index.html")
def home():
    data = _data()
    data["home"] = open("Home.md").read()
    return render_template("index.html", **data)


@app.route("/registration.html")
def registration():
    data = _data()
    data["registration"] = open("sitedata/registration.md").read()
    return render_template("registration.html", **data)

@app.route("/onlinepresence.html")
def onlinepresence():
    data = _data()
    data["onlinepresence"] = open("sitedata/onlinepresence.md").read()
    return render_template("onlinepresence.html", **data)


@app.route("/invoice.html")
def invoice():
    data = _data()
    data["invoice"] = open("sitedata/invoice.md").read()
    return render_template("invoice.html", **data)


@app.route("/venue.html")
def venue():
    data = _data()
    data["venue"] = open("sitedata/venue.md").read()
    return render_template("venue.html", **data)


@app.route("/presenters.html")
def presenters():
    data = _data()
    data["presenters"] = open("sitedata/presenters.md").read()
    return render_template("presenters.html", **data)


@app.route("/local.html")
def local():
    data = _data()
    data["local"] = open("sitedata/local.md").read()
    return render_template("local.html", **data)


@app.route("/organizers.html")
def organizers():
    data = _data()
    data["committee"] = site_data["committee"]["committee"]
    return render_template("organizers.html", **data)


@app.route("/speakers.html")
def speakers():
    data = _data()
    data["speakers"] = site_data["speakers"]["speakers"]
    return render_template("speakers.html", **data)


@app.route("/calls.html")
def calls():
    data = _data()
    data["calls"] = site_data["calls"]["calls"]
    for call in data["calls"]:
        call["bodytext"] = open(call["body"]).read()
    return render_template("calls.html", **data)


@app.route("/resource_statement.html")
def resource_statement():
    data = _data()
    data["resource_statement"] = open("sitedata/resource_statement.md").read()
    return render_template("resource_statement.html", **data)


@app.route("/help.html")
def about():
    data = _data()
    data["FAQ"] = site_data["faq"]["FAQ"]
    return render_template("help.html", **data)


@app.route("/workshops.html")
def workshops():
    data = _data()
    data["workshops"] = open("sitedata/workshops.md").read()
    return render_template("workshops_preliminary.html", **data)


@app.route("/papers.html")
def papers():
    data = _data()
    data["papers"] = site_data["papers"]
    data["papers"].sort(key=lambda x: x["title"])
    return render_template("papers.html", **data)


@app.route("/calendar.html")
def schedule():
    data = _data()
    data["days"] = by_date
    out = render_template("schedule.html", **data)
    return out


# @app.route("/workshops.html")
# def workshops():
#     data = _data()
#     data["workshops"] = [
#         format_workshop(workshop) for workshop in site_data["workshops"]
#     ]
#     return render_template("workshops.html", **data)
#
#
# @app.route("/tutorials.html")
# def tutorials():
#     data = _data()
#     data["workshops"] = [
#         format_workshop(tutorial) for tutorial in site_data["tutorials"]
#     ]
#     return render_template("workshops.html", **data)
#
#
# @app.route("/panels.html")
# def panels():
#     data = _data()
#     data["workshops"] = [
#         format_workshop(panel) for panel in site_data["panels"]
#     ]
#     return render_template("workshops.html", **data)
#
#
# @app.route("/hackathons.html")
# def hackathons():
#     data = _data()
#     data["workshops"] = [
#         format_workshop(hackathon) for hackathon in site_data["hackathons"]
#     ]
#     return render_template("workshops.html", **data)
#
#
# @app.route("/genchal.html")
# def genchal():
#     data = _data()
#     data["workshops"] = [
#         format_workshop(genchal) for genchal in site_data["genchal"]
#     ]
#     return render_template("workshops.html", **data)
#
#


@app.route("/sponsors.html")
def sponsors():
    data = _data()
    data["platinumsponsors"] = site_data["platinumsponsors"]
    data["goldsponsors"] = site_data["goldsponsors"]
    data["silversponsors"] = site_data["silversponsors"]
    data["bronzesponsors"] = site_data["bronzesponsors"]
    return render_template("sponsors.html", **data)


def extract_list_field(v, key):
    value = v.get(key, "")
    if isinstance(value, list):
        return value
    else:
        return value.split("|")


def format_paper(v):
    v["authors"] = extract_list_field(v, "authors")
    # dt = datetime.fromisoformat(v["start"])
    # v["time"] = dt.strftime("%A %m/%d %H:%M CEST")
    # v["short_time"] = dt.strftime("%H:%M EST")
    v["title"] = v["title"].title()
    v["title"] = re.sub(r"Nlg", "NLG", v["title"])
    return v


def format_workshop(v):
    v["organizers"] = extract_list_field(v, "authors")
    dt = datetime.fromisoformat(v["start"])
    v["time"] = dt.strftime("%A %m/%d %H:%M CEST")
    return v


# ITEM PAGES


@app.route("/poster_<poster>.html")
def poster(poster):
    uid = poster
    v = by_uid["papers"][uid]
    data = _data()
    data["paper"] = v
    return render_template("poster.html", **data)


# FRONT END SERVING


@app.route("/papers.json")
def paper_json():
    json = []
    for v in site_data["papers"]:
        json.append(v)
    json.sort(key=lambda x: x["title"])

    return jsonify(json)


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


@app.route("/serve_<path>.json")
def serve(path):
    return jsonify(site_data[path])


# --------------- DRIVER CODE -------------------------->
# Code to turn it all static


@freezer.register_generator
def generator():
    for paper in site_data["papers"]:
        yield "poster", {"poster": str(paper["UID"])}

    for key in site_data:
        yield "serve", {"path": key}


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")

    parser.add_argument(
        "--build",
        action="store_true",
        default=False,
        help="Convert the site to static assets",
    )

    parser.add_argument(
        "-b",
        action="store_true",
        default=False,
        dest="build",
        help="Convert the site to static assets",
    )

    parser.add_argument("path", help="Pass the JSON data path and run the server")

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_arguments()

    site_data_path = args.path
    extra_files = main(site_data_path)

    if args.build:
        freezer.freeze()
    else:
        debug_val = False
        if os.getenv("FLASK_DEBUG") == "True":
            debug_val = True

        app.run(port=5000, debug=debug_val, extra_files=extra_files)
