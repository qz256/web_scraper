import datetime as dt
import pandas as pd
from zillow_scraper.extract import extract_housing_info

url_list = [
    "https://www.zillow.com/homedetails/11-Angier-Cir-Newton-MA-02466/56310894_zpid",
    "https://www.zillow.com/homedetails/15-Woodbine-Ter-Newton-MA-02466/56309502_zpid",
    "https://www.zillow.com/homedetails/211-Melrose-St-Newton-MA-02466/56309621_zpid",
]

if __name__ == '__main__':

    summary = pd.DataFrame()
    for url in url_list:
        housing_info = extract_housing_info(url)
        summary = pd.concat([summary, pd.DataFrame([housing_info])])
    summary.to_excel(f"data/{dt.datetime.strftime(dt.datetime.today().date(), '%Y%m%d')}_house_listing.xlsx", index=False)