import datetime
import time
import json
import os
from tableauscraper import TableauScraper as TS


def scrape_tableau(ts: TS, url: str, out_path: str, date: str, date_check: bool = False) -> None:
    start = time.time()
    ts.loads(url)
    workbook = ts.getWorkbook()
    dashboard_tables = {}
    for t in workbook.worksheets:
        # Check if dashboard latest data date is today by checking cases timeline
        if date_check and t.name == "D_NewTL":
            if not (t.data["DAY(txn_date)-value"] == f"{date} 00:00:00").iloc[-1]:
                print("Dashboard date mismatched from query date:", date)
                raise AssertionError
        dashboard_tables[t.name] = t.data.to_dict(orient="records")
    with open(os.path.join(out_path, f"{date}.json"), "w+", encoding="utf-8") as f:
        json.dump(dashboard_tables, f, ensure_ascii=False, indent=2)
    print("Time:", round(time.time() - start, 2))


if __name__ == '__main__':
    date = str(datetime.datetime.now().date())
    out_path = "../wiki/tableau_dump"
    os.makedirs(out_path, exist_ok=True)
    url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles-w"
    scrape_tableau(TS(), url, out_path, date, date_check=True)
