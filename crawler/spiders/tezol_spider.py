import requests
import scrapy
import json

class TezolSpider(scrapy.Spider):
    name = 'tezol'
    start_urls = ['https://www.tezolmarket.com/Home/GetProductQueryResult']
    request_url = 'https://www.tezolmarket.com/Home/GetProductQueryResult'
    endpoint_url = 'http://127.0.0.1:8000/'

    def parse(self, response, **kwargs):
        api_response = requests.post(self.request_url, json={
        "AppliedAttributeValueIds": None,
        "SearchTerm": None,
        "SearchPrice": None,
        "PageIndex": 0,
        "CategoryId": 46,
        "AppliedBrandIds": None
        })
        resp_in_json = api_response.json()
        deserialized = resp_in_json.get("Products")
        for product in deserialized:
            temp_dic = {}
            temp_dic['id'] = product['ProductId']
            temp_dic['title'] = product['FullName'].replace(' ', '-')
            temp_dic['price'] = int(product['FinalUnitPrice'])*10
            temp_dic['base_price'] = int(product['FinalUnitPrice'])*10
            temp_dic['vendor'] = "tezol"
            r = requests.post(self.endpoint_url, json=temp_dic)
