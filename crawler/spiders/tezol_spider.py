import scrapy
from scrapy import Request
import json
from scrapy.http import Response


# noinspection PyDictCreation
class TezolCategorySpider(scrapy.Spider):
    name = 'tezolCategory'
    start_urls = ['https://www.tezolmarket.com']
    website_homepage = 'https://www.tezolmarket.com'
    endpoint_url = 'http://127.0.0.1:8000/api/'

    def parse(self, response, **kwargs):
        categories = response.css('ul.children.col-xs-12.text-right.wrap').css('div.menuColWrap')
        for menuColRap in categories:
            category_name = menuColRap.css('img.menuImg.menuImgHeight').attrib['alt']
            yield self.data_sender(None, category_name)
            menu_cols = menuColRap.css('div.menuCol')
            for menuCol in menu_cols:
                sub_category_name = menuCol.css('h4::text')
                super_category = category_name
                yield self.data_sender(super_category, sub_category_name)
                sub_menus = menuCol.css('ul.subMenu').css('li')
                for sub_menu in sub_menus:
                    sub_sub_category_name = sub_menu.css('a::text')
                    parent_category = sub_category_name
                    yield self.data_sender(parent_category, sub_sub_category_name)

    def data_sender(self, super_category, name):
        temp = {
            'name': name,
            'super_category': super_category
        }
        return Request(self.endpoint_url, body=json.dumps(temp), method='POST',
                       headers={'Content-Type': 'application/json'})


class TezolProductCrawler(scrapy.Spider):
    name = 'tezolProduct'
    endpoint_url = 'http://127.0.0.1:8000/api/'
    request_url = 'https://www.tezolmarket.com/Home/GetProductQueryResult'
    product_details = 'https://www.tezolmarket.com/Product/product_id/slug?returnUrl=/Category/category_id/'

    def start_requests(self):
        yield Request(self.request_url, body=json.dumps({
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": 0,
            "CategoryId": 46,
            "AppliedBrandIds": None
        }), method='POST', headers={'Content-Type': 'application/json'})

    def product_website_api_request(self, page_number, category_id):
        yield Request(self.request_url, body=json.dumps({
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": page_number,
            "CategoryId": category_id,
            "AppliedBrandIds": None
        }), method='POST', headers={'Content-Type': 'application/json'})

    def parse(self, response, **kwargs):
        page_number = 0
        for category_id in range(4):
            while response is not None:
                self.product_website_api_request(page_number, category_id)
                self.product_slug_index_scraper(response)
                page_number = page_number + 1

    def product_slug_index_scraper(self, response):
        response_in_json = json.loads(response.body)
        products = response_in_json.get("Products")
        for product in products:
            product_instance = {}
            product_instance['id'] = product['ProductId']
            product_instance['name'] = product['FullName']
            product_instance['price'] = int(product['FinalUnitPrice']) * 10
            product_instance['base_price'] = int(product['FinalUnitPrice']) * 10
            product_instance['vendor'] = "tezol"
            self.product_brand_scraper(product_instance, response)

    def product_brand_scraper(self, product_instance, response):
        product_instance['id']
        product_instance['id']
        yield Response(self.product_details)
