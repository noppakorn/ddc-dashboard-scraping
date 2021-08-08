import json
import os
import datetime
import requests
import csv
from util import json_load


def get_date_data(date: str, key_mapping: dict) -> dict:
    dashboard_data = json_load(f"../wiki/tableau_dump/{date}.json")
    date_data = {}
    for table, new_name in key_mapping.items():
        # For testing data the table have separate update date
        if table == "D_Lab":
            if len(dashboard_data[table]) < 1:
                lab_avg, lab_date = None, None
            else:
                lab_avg, lab_date = dashboard_data[table][0].values()
            if lab_avg == "%null%" or lab_avg is None or lab_date == "%null%" or lab_date is None:
                lab_avg, lab_date = None, None
            else:
                #lab_avg = round(float()
                lab_avg = round(float(str(lab_avg).replace(",", "")))
                lab_date = str(datetime.datetime.strptime(lab_date, "%m/%d/%Y").date())
            date_data["average_test"] = lab_avg
            date_data["average_test_update_date"] = lab_date
        else:
            if len(dashboard_data[table]) < 1:
                curr_value = None
            else:
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
        "D_ATK": "new_atk_cases",
        "D_ATKACM": "cumulative_atk_cases",
        "D_Medic": "hospitalized",
        "D_Hospital": "in_hospital",
        "D_HospitalField": "in_hospital_field",
        "D_Severe": "severe_cases",
        "D_SevereTube": "severe_cases_tube",
        "D_Walkin": "new_walkin_cases",
        "D_WalkinACM": "cumulative_walkin_cases",
        "D_Proact": "new_proactive_cases",
        "D_ProactACM": "cumulative_proactive_cases",
        "D_Thai": "new_thai_cases",
        "D_ThaiACM": "cumulative_thai_cases",
        "D_NonThai": "new_foreign_cases",
        "D_NonThaiACM": "cumulative_foreign_cases",
        "D_Prison": "new_prison_cases",
        "D_PrisonACM": "cumulative_prison_cases",
        "D_Recov": "new_recovered",
        "D_RecovACM": "cumulative_recovered",
        "D_Lab": "testing_data",
    }
    date = str(datetime.datetime.now().date())

    print("Processing:", date)
    today_data = {"date": date}
    today_data.update(get_date_data(date, key_mapping))

    prev_json = "https://raw.githubusercontent.com/wiki/noppakorn/ddc-dashboard-scraping/dataset/national-timeseries.json"
    req = requests.get(prev_json)
    json_data = req.json()
    if json_data[-1]["date"] == date :
        print("Data for:", date, "already exist in json, replacing.")
        json_data[-1] = today_data
    else :
        json_data.append(today_data)

    out_path = "../wiki/dataset/"
    os.makedirs(out_path, exist_ok=True)
    with open(os.path.join(out_path, "national-timeseries.json"), "w+") as fout:
        json.dump(json_data, fout, ensure_ascii=False, indent=2)

    fieldnames = ["date"] + list(key_mapping.values()) + ["average_test", "average_test_update_date"]
    with open(os.path.join(out_path, "national-timeseries.csv"), "w+", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(json_data)
