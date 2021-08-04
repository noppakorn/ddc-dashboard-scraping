import glob
import os
from tableauscraper import TableauScraper as TS
from util import json_load
from scrape_tablueau_data import scrape_tablueau
from multiprocessing.pool import ThreadPool


def scrape_wrapper(parameters: tuple):
    print("Processing:", parameters[1])
    ts = TS()
    scrape_tablueau(ts, url=parameters[0], out_path=out_path, date=parameters[1])


if __name__ == "__main__":

    url_dict = {}
    for i in glob.glob("../dashboard_links/covid-dashboard-link-2021-*.json"):
        url_dict.update(json_load(i))

    out_path = "../wiki/tableau_dump"
    os.makedirs(out_path, exist_ok=True)
    scrape_parameters = []
    for date, url in url_dict.items():
        date = date.split("/")
        date = f"{date[2]}-{date[0]}-{date[1]}"
        scrape_parameters.append((url, date))

    with ThreadPool(16) as p:
        p.map(scrape_wrapper, scrape_parameters)

