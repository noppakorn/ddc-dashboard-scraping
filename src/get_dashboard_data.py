import glob
import os
from tableauscraper import TableauScraper as TS
import time
from util import json_load, df_to_json


if __name__ == "__main__":
    ts = TS()


    url_dict = {}
    for i in glob.glob("../json/covid-dashboard-link-2021-*.json"):
        url_dict.update(json_load(i))

    for date, url in url_dict.items():
        start = time.time()
        date = date.split("/")
        date = f"{date[2]}-{date[0]}-{date[1]}"
        print("Processing:", date)
        ts.loads(url)
        workbook = ts.getWorkbook()
        out_path = f"../tablueau_dump/{date}"
        os.makedirs(out_path, exist_ok=True)
        for t in workbook.worksheets:
            df_to_json(t.data, os.path.join(out_path, f"{t.name}.json"))
        print("Time:", round(time.time() - start, 2))
