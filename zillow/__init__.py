from zillow_scraper.extract import extract_housing_info

if __name__ == '__main__':
    url = f"https://www.zillow.com/homedetails/211-Melrose-St-Newton-MA-02466/56309621_zpid"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0",
        "Referer": "https://www.google.com"
    }
    housing_info = extract_housing_info(url, headers)
