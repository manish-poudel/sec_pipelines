import json


class CompanyDataGenerator:

    # Function to get data by ticker

    @staticmethod
    def _get_company_by_ticker(ticker_value, companies_list):
        for company in companies_list:
            if company['ticker'] == ticker_value:
                return company
        return None

    def get_tech_companies(self):
        tech_companies_path = "assets/tech_companies.txt"
        sec_companies_path = "assets/sec_companies.json"
        data = []

        # Open sec companies json files
        sec_companies_file = open(sec_companies_path)
        sec_companies_json = json.load(sec_companies_file)

        # Create list
        sec_companies_list = sec_companies_json.values()
        with open(tech_companies_path, "r") as file:
            for line in file:
                parts = line.strip().split("\t")

                ticker = parts[1]

                sec_company = self._get_company_by_ticker(ticker, sec_companies_list)

                if sec_company is not None:
                    cik = sec_company.get("cik_str")
                    company_name = sec_company.get("title")

                    data.append({
                        "ticker": ticker,
                        "cik": cik,
                        "company_name": company_name
                    })

        with open("assets/sec_tech_companies.json", 'w') as file:
            json.dump(data, file, indent=4)



