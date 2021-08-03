import glob
import os
from tableauscraper import TableauScraper as TS
import time
from util import json_load, df_to_json
from scrape_tablueau_data import scrape_tablueau


if __name__ == "__main__":
    ts = TS()


    url_dict = {}
    for i in glob.glob("../dashboard_links/covid-dashboard-link-2021-*.json"):
        url_dict.update(json_load(i))

    for date, url in url_dict.items():
        date = date.split("/")
        date = f"{date[2]}-{date[0]}-{date[1]}"
        print("Processing:", date)
        out_path = f"../wiki/tablueau_dump/{date}"
        scrape_tablueau(ts, url, out_path)
