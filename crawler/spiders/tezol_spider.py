import requests
import scrapy
import json

class TezolSpider(scrapy.Spider):
    name = 'tezol'
    start_urls = ['https://www.tezolmarket.com/Home/GetProductQueryResult']
    request_url = 'https://www.tezolmarket.com/Home/GetProductQueryResult'

    def parse(self, response, **kwargs):
        api_response = requests.post(self.request_url, json={
        "AppliedAttributeValueIds": None,
        "SearchTerm": None,
        "SearchPrice": None,
        "PageIndex": 0,
        "CategoryId": 46,
        "AppliedBrandIds": None
        })
        print(api_response.json())