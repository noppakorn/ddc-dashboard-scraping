import json
import os
import pandas as pd
import csv
from build_national_timeseries import get_date_data


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
    }
    timeframe = [str(date.date()) for date in pd.date_range("2021-01-01", "2021-08-03")]
    timeseries = []
    for date in timeframe:
        curr_data = {"date": date}
        curr_data.update(get_date_data(date, key_mapping))
        timeseries.append(curr_data)

    out_path = "../wiki/dataset/"
    os.makedirs(out_path, exist_ok=True)

    with open(os.path.join(out_path, "national-timeseries.json"), "w+", encoding="utf-8") as json_file:
        json.dump(timeseries, json_file, ensure_ascii=False, indent=2)

    fieldnames = ["date"] + list(key_mapping.values())
    with open(os.path.join(out_path, "national-timeseries.csv"), "w+", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(timeseries)
