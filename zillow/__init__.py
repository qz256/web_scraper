from zillow_scraper.extract import extract_housing_info

if __name__ == '__main__':
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:78.0)   Gecko/20100101 Firefox/78.0",
               "Referer": "https://www.google.com"}

    url = f"https://www.zillow.com/homedetails/211-Melrose-St-Newton-MA-02466/56309621_zpid//"
    housing_info = extract_housing_info(url, headers)
    for home in housing_info:
        print(home['address'], home['price'], home['beds'], home['baths'], home['sqft'])
