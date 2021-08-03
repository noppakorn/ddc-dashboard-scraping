from tableauscraper import TableauScraper as TS

if __name__ == "__main__":
    #url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles-w?:embed=y&:toolbar=n&:display_count=n&:origin=viz_share_link"
    url = "https://public.tableau.com/views/SATCOVIDDashboard/1-dash-tiles-w"
    ts = TS()
    ts.loads(url)

    workbook = ts.getWorkbook()
    workbook = workbook.setParameter("param_date", "2021-08-02")

    for t in workbook.worksheets:
        print(f"worksheet name : {t.name}") #show worksheet name
        print(t.data) #show dataframe for this worksheet)
