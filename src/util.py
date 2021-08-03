import json
import pandas as pd

def json_load(file_path):
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


def df_to_json(df: pd.DataFrame, path: str) -> None:
    with open(path, "w+", encoding="utf-8") as fout:
        df.to_json(fout, force_ascii=False, orient="records", indent=2)

