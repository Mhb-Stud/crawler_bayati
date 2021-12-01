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
    response = None

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
        self.product_scraper(response_in_json)
        Request('https://www.tezolmarket.com')
        categories = response.css('ul.children.col-xs-12.text-right.wrap').css('div.menuColWrap')
        for menuColRap in categories:
            category_name = menuColRap.css('img.menuImg.menuImgHeight').attrib['alt']
            self.data_sender(None, category_name)
            menu_cols = menuColRap.css('div.menuCol')
            for menuCol in menu_cols:
                sub_category_name = menuCol.css('h4::text')
                super_category = category_name
                self.data_sender(super_category, sub_category_name)
                sub_menus = menuCol.css('ul.subMenu').css('li')
                for sub_menu in sub_menus:
                    sub_sub_category_name = sub_menu.css('a::text')
                    parent_category = sub_category_name
                    self.data_sender(parent_category, sub_sub_category_name)

    def data_sender(self, super_category, category_name):
        temp_dic = {
            'category_name': category_name,
            'super_category': super_category
        }
        yield Request(self.endpoint_url, body=json.dumps(temp_dic), method='POST',
                      headers={'Content-Type': 'application/json'})

    def product_scraper(self, response_in_json):
        products = response_in_json.get("Products")
        for product in products:
            temp_dic = {}
            temp_dic['id'] = product['ProductId']
            temp_dic['title'] = product['FullName'].replace(' ', '-')
            temp_dic['price'] = int(product['FinalUnitPrice']) * 10
            temp_dic['base_price'] = int(product['FinalUnitPrice']) * 10
            temp_dic['vendor'] = "tezol"
            yield Request(self.endpoint_url, body=json.dumps(temp_dic), method='POST',
                          headers={'Content-Type': 'application/json'})
