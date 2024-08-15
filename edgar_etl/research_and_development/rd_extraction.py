import os
import time
from datetime import datetime

from edgar_etl.abstracts.edgar_extraction import EdgarExtraction
from services.sec_xbrl_services import SECXBRLServices

from utilities.string_utilities import format_cik
from ..enums.research_expense_type import ResearchExpenseType
import pandas as pd


class RDExtraction(EdgarExtraction):

    def __init__(self, user_agent):
        self._user_agent = user_agent

    def _xbrl_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        return self._extract_rd_from_xbrl(cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days)

    def _gen_ai_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        print("Not implemented")

    def _delegate_extraction(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        print("Not implemented")
        df = self._extract_rd_from_xbrl(cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days)
        # Now check for missing and delegate to llama ji

    def _extract_rd_from_xbrl(self, cik_list, from_date, to_date, request_delay_sec, use_cache, cache_max_days):
        file_name = f"rd_{from_date}_{to_date}.csv"
        file_path = f"data/rd/extracted/{file_name}"

        # if user wants to use cache
        if use_cache and os.path.isfile(file_path):
            stat_info = os.stat(file_path)
            current_time = datetime.now()
            time_difference = current_time - datetime.fromtimestamp(stat_info.st_ctime)
            if time_difference.days <= cache_max_days:
                print("Returning cache...")
                return pd.read_csv(file_path)

        df = None

        cik_len = len(cik_list)
        print(cik_list)
        for index, cik in enumerate(cik_list):
            # Delay request by certain milliseconds to prevent rapid ping to sec server
            print(f"Getting rd value of {cik}")
            cik_df = self._get_rd_from_xbrl(cik, from_date, to_date)
            if cik_df is None:
                continue
            elif df is None:
                df = cik_df
            else:
                df = pd.concat([df, cik_df], ignore_index=True)

            print(f"Completed: {index + +1}/{cik_len}")
            print(f"sleeping for {request_delay_sec}")
            time.sleep(request_delay_sec)
            print("woke up..")

        return df

    def _get_rd_from_xbrl(self, cik, from_date, to_date):
        try:
            xbrl_services = SECXBRLServices(self._user_agent)
            company_facts_content = xbrl_services.get_company_facts(format_cik(cik)).json()
            # Check for  us-gaap key in xbrl
            if "facts" in company_facts_content and "us-gaap" in company_facts_content["facts"]:
                incurred_df = self._get_rd(ResearchExpenseType.incurred.value, from_date, to_date,
                                           company_facts_content["facts"]["us-gaap"])
                incurred_df["cik"] = cik
                incurred_df["source"] = "xbrl"
                return incurred_df
            else:
                return None

        except Exception as e:
            print(e)
            return None

    @staticmethod
    def _get_rd(expense_type, from_date, to_date, data):
        try:
            expense_list = data[expense_type["tag"]]["units"]["USD"]
            df = pd.DataFrame(expense_list)
            df = df[(df['form'].isin(['10-Q', '10-K'])) & (df['fy'].between(from_date, to_date))]
            df = df[['fy', 'val', 'fp', 'filed']]
            df = df.rename(columns={
                "fy": "fiscal_year",
                "fp": "fiscal_period",
                "val": expense_type["readable_name"]
            })
            return df
        except Exception as e:
            print(e)
            return None
