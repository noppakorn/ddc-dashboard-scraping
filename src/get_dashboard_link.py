from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import time
import json
import pandas as pd
import sys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,5000")


def get_date_share_link(wd: webdriver.Chrome, date: str) -> str:
    wd.switch_to.default_content()
    print("Changing Date to:", date)
    wd.find_element_by_id("dpick").send_keys(date)
    frame = wd.find_element(By.XPATH, "//div[@id='tableauPlaceholder']/iframe")
    wd.switch_to.frame(frame)
    # Wait till loading finished
    time.sleep(15)
    share_button = wd.find_element(By.XPATH, "//div[@id='share-ToolbarButton']").click()
    share_link = wd.find_elements(By.XPATH, "//input[@class='tabTextInputViewInputElement tab-shareInput']")
    out = share_link[1].get_attribute("value")
    # Close share window
    wd.find_element(By.XPATH, "//button[@class='f1odzkbq fyvorft fdxv97z low-density']").click()
    return out


if __name__ == '__main__':
    wd = webdriver.Chrome("chromedriver", options=chrome_options)
    wd.get("https://ddc.moph.go.th/covid19-dashboard/")
    time.sleep(5)
    start, end = sys.argv[1], sys.argv[2]
    share_link_dict = {}
    for dto in pd.date_range(start, end):
        date_to_scrape = f"{str(dto.month).zfill(2)}/{str(dto.day).zfill(2)}/{dto.year}"
        share_link = get_date_share_link(wd, date_to_scrape)
        share_link_dict[date_to_scrape] = share_link
        print(date_to_scrape, ":", share_link)
    wd.close()
    out_path = "../dashboard_links"
    os.makedirs(out_path, exist_ok=True)
    with open(os.path.join(out_path, f"covid-dashboard-link-{start}-{end}.dashboard_links"), "w+", encoding="utf-8") as fout:
        json.dump(share_link_dict, fout, ensure_ascii=False, indent=2)
