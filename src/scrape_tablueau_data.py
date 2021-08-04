import datetime
import time
import json
import os
from tableauscraper import TableauScraper as TS
from util import df_to_json

def scrape_tablueau(ts: TS, url: str, out_path: str, date: str) -> None:
    start = time.time()
    ts.loads(url)
    workbook = ts.getWorkbook()
    os.makedirs(out_path, exist_ok=True)
    l = {}
    for t in workbook.worksheets:
        l[t.name] = t.data.to_dict(orient="records")
    with open(os.path.join(out_path, f"{date}.json"), "w+", encoding="utf-8") as f:
        json.dump(l, f, ensure_ascii=False, indent=2)
    print("Time:", round(time.time() - start, 2))

if __name__ == '__main__':
    date = str(datetime.datetime.now().date())
    out_path = f"../wiki/tableau_dump"
    url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles-w"
    scrape_tablueau(TS(), url, out_path, date)
