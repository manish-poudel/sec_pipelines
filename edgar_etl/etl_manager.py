import json

from edgar_etl.research_and_development.rd_extraction import RDExtraction
from edgar_etl.research_and_development.rd_transformer import RDTransformer
import pandas as pd


# ETL Manager handles all the process such as extracting, transforming and loading

class ETLManager:

    def __init__(self):
        self._user_agent = "omekus.co@gmail.com"

    # Method that run's process for getting R&D value
    def run_RDProcess(self):
        # Get the list of all tech companies we have in sec_tech_companies json file
        with open("assets/sec_tech_companies.json", "r") as tech_companies:
            companies = json.load(tech_companies)
            cik_list = []
            for company in companies:
                cik_list.append(company["cik"])
            rd_extraction = RDExtraction(user_agent=self._user_agent)

            # EXTRACT DATA
            from_date = 2013
            to_date = 2023
            df = rd_extraction.extract(cik_list, from_date=from_date, to_date=to_date,
                                       extraction_type="xbrl", request_delay_sec=1, use_cache=True,
                                       cache_max_days=2)

            # save extracted data
            file_name = f"rd_{from_date}_{to_date}.csv"
            file_path = f"data/rd/extracted/{file_name}"
            df.to_csv(file_path, index=False)

            # TRANSFORM DATA
            transformed_data = RDTransformer.compute_zscore(df=df)
            # add ticker
            companies_df = pd.DataFrame(companies)
            merged_df = pd.merge(transformed_data, companies_df[['cik', 'ticker']], on='cik', how='left')
            merged_df.rename(columns={'ticker': 'symbol'}, inplace=True)

            print(len(merged_df))
            # LOAD DATA
            merged_df.to_csv(f"data/rd/transformed/{file_name}", index=False)



