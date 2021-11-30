import scrapy
from scrapy import Request
import json
from scrapy.http import Response


# noinspection PyDictCreation
class TezolSpider(scrapy.Spider):
    name = 'tezol'
    # start_urls = ['https://www.tezolmarket.com/Home/GetProductQueryResult']
    request_url = 'https://www.tezolmarket.com/Home/GetProductQueryResult'
    endpoint_url = 'http://127.0.0.1:8000/api/'

    def start_requests(self):
        yield Request(self.request_url, body=json.dumps({
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": 0,
            "CategoryId": 46,
            "AppliedBrandIds": None
        }), method='POST', headers={'Content-Type': 'application/json'})

    def parse(self, response, **kwargs):
        response_in_json = json.loads(response.body)
        products = response_in_json.get("Products")
        for product in products:
            temp_dic = {}
            temp_dic['id'] = product['ProductId']
            temp_dic['title'] = product['FullName'].replace(' ', '-')
            temp_dic['price'] = int(product['FinalUnitPrice']) * 10
            temp_dic['base_price'] = int(product['FinalUnitPrice']) * 10
            temp_dic['vendor'] = "tezol"
            yield Request(self.endpoint_url, body=json.dumps(temp_dic), method='POST', headers={'Content-Type': 'application/json'})



