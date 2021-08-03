import datetime
import time
import json
import os
import pandas as pd
from tableauscraper import TableauScraper as TS
from util import df_to_json

def scrape_tablueau(ts: TS, url: str, out_path: str) -> None:
    start = time.time()
    ts.loads(url)
    workbook = ts.getWorkbook()
    os.makedirs(out_path, exist_ok=True)
    for t in workbook.worksheets:
        df_to_json(t.data, os.path.join(out_path, f"{t.name}.json"))
    print("Time:", round(time.time() - start, 2))

if __name__ == '__main__':
    date = str(datetime.datetime.now().date())
    date = "2021-08-03"
    out_path = f"../wiki/tablueau_dump/{date}"
    url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles-w"
    scrape_tablueau(TS(), url, out_path)
