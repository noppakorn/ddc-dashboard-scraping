import json
import os
import datetime
import requests
from util import json_load


def get_date_data(date: str, key_mapping: dict) -> dict:
    dashboard_data = json_load(f"../wiki/tableau_dump/{date}.json")
    date_data = {}
    for table, new_name in key_mapping.items():
        curr_value = tuple(dashboard_data[table][0].values())[0]
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
        "D_Severe": "severe_cases",
        "D_SevereTube": "severe_cases_tube",
        "D_Walkin": "new_walkin_cases",
        "D_WalkinACM": "cumulative_walkin_cases",
    }
    date = str(datetime.datetime.now().date())
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
