import json
import os
import pandas as pd
from build_national_timeseries import get_date_data


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
    timeframe = [str(date.date()) for date in pd.date_range("2021-01-01", "2021-08-02")]
    out = []
    for date in timeframe:
        curr_data = {"date": date}
        curr_data.update(get_date_data(date, key_mapping))
        out.append(curr_data)

    out_path = "../wiki/dataset/"
    os.makedirs(out_path, exist_ok=True)
    with open(os.path.join(out_path, "national-timeseries.json"), "w+", encoding="utf-8") as fout:
        json.dump(out, fout, ensure_ascii=False, indent=2)
