import requests as r
from bs4 import BeautifulSoup

class Indicators:
    type = ""
    def __init__(self, type):
        self.type = type

    def getData(self):
        html = r.get(self.dataEndpoint())
        soup = BeautifulSoup(html.text, 'html.parser')
        l = soup.select(self.scrapperSelector())
        return l

    def dataEndpoint(self):
        if self.type == "cci":
            return "https://ycharts.com/indicators/us_consumer_sentiment_index"
        elif self.type == "jobless":
            return "https://ycharts.com/indicators/us_unemployment_rate"
        elif self.type == "pe":
            return "https://ycharts.com/indicators/sp_500_pe_ratio"
        elif self.type == "dollarindex":
            return "https://ycharts.com/indicators/trade_weighted_us_dollar_index_broad_goods_and_services"
        elif self.type == "inflation":
            return "https://ycharts.com/indicators/us_inflation_rate"
        elif self.type == "putcall":
            return "https://ycharts.com/indicators/cboe_equity_put_call_ratio"
        elif self.type == "manufacturing":
            return "https://ycharts.com/indicators/us_pmi"

    def scrapperSelector(self):
        if self.type == "cci" or self.type == "jobless" or self.type == "pe" or self.type == "dollarindex" or self.type == "inflation" or self.type == "putcall" or self.type == "manufacturing":
            return "div[class='page-body'] > div > div:nth-child(1) > div:nth-child(4) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > table"
