import json
import os
import pandas as pd
import datetime
import requests
from util import json_load


def get_date_data(date: str, key_mapping: dict) -> dict:
    date_data = {}
    for table, new_name in key_mapping.items():
        path = f"../wiki/tablueau_dump/{date}/{table}.json"
        curr_value = tuple(json_load(path)[0].values())[0]
        if curr_value == "%null%":
            curr_value = None
        date_data[new_name] = curr_value
    return date_data

if __name__ == '__main__':
    key_mapping = {
        "D_New": "new_cases",
        "D_NewACM": "cumulative_cases",
        "D_Death": "new_deaths",
        "D_DeathACM": "cumulative_deaths",
        "D_Medic": "hospitalized",
        "D_ATK": "new_atk_cases",
        "D_ATKACM": "cumulative_atk_cases",
    }
    date = str(datetime.datetime.now().date())
    date = "2021-08-03"
    prev_data = "https://raw.githubusercontent.com/wiki/noppakorn/ddc-dashboard-scraping/dataset/national-timeseries.json"
    req = requests.get(prev_data)
    json_data = req.json()
    today_data = {"date": date}
    today_data.update(get_date_data(date, key_mapping))
    json_data.append(today_data)
    out_path = "../wiki/dataset/"
    os.makedirs(out_path, exist_ok=True)
    with open(os.path.join(out_path, "national-timeseries.json"), "w+") as fout:
        json.dump(json_data, fout, ensure_ascii=False, indent=2)
