import scrapy
from scrapy import Request
import json
import requests
from scrapy.http import Response


# noinspection PyDictCreation
# class TezolCategorySpider(scrapy.Spider):
#     name = 'tezolCategory'
#     start_urls = ['https://www.tezolmarket.com']
#     website_homepage = 'https://www.tezolmarket.com'
#     endpoint_url = 'http://127.0.0.1:8000/api/'
#
#     def parse(self, response, **kwargs):
#         categories = response.css('ul.children.col-xs-12.text-right.wrap').css('div.menuColWrap')
#         for menuColRap in categories:
#             category_name = menuColRap.css('img.menuImg.menuImgHeight').attrib['alt']
#             yield self.data_sender(None, category_name)
#             menu_cols = menuColRap.css('div.menuCol')
#             for menuCol in menu_cols:
#                 sub_category_name = menuCol.css('h4::text')
#                 super_category = category_name
#                 yield self.data_sender(super_category, sub_category_name)
#                 sub_menus = menuCol.css('ul.subMenu').css('li')
#                 for sub_menu in sub_menus:
#                     sub_sub_category_name = sub_menu.css('a::text')
#                     parent_category = sub_category_name
#                     yield self.data_sender(parent_category, sub_sub_category_name)
#
#     def data_sender(self, super_category, name):
#         temp = {
#             'name': name,
#             'super_category': super_category
#         }
#         return Request(self.endpoint_url, body=json.dumps(temp), method='POST',
#                        headers={'Content-Type': 'application/json'})


class TezolProductCrawler(scrapy.Spider):
    name = 'tezolProduct'
    endpoint_url = 'http://127.0.0.1:8000/api/'
    request_url = 'https://www.tezolmarket.com/Home/GetProductQueryResult'
    product_details = 'https://www.tezolmarket.com/Product/product_id/slug?returnUrl=/Category/category_id/'
    page_number = 1
    category = 1

    def start_requests(self):
        yield Request(self.request_url, body=json.dumps({
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": 0,
            "CategoryId": 1,
            "AppliedBrandIds": None
        }), method='POST', headers={'Content-Type': 'application/json'})

    def product_scraper_caller(self, page_number, category_id):
        return Request(self.request_url, body=json.dumps({
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": page_number,
            "CategoryId": category_id,
            "AppliedBrandIds": None
        }), method='POST', headers={'Content-Type': 'application/json'}, callback=self.product_scraper)

    def page_number_saver(self, category_id):
        """the only reason i'm using requests library here is for each category i have to get the page number from
        the api request to then loop through the pages sending an api request to each page and finally crawl their data
        because scrapy.Request uses concurrency i can't use it since i need to have number of pages before i go through
        with my code and only 119 times i have to run page_number_saver and it doesn't create a bottleneck
        """
        api_response = requests.post(self.request_url, json={
            "AppliedAttributeValueIds": None,
            "SearchTerm": None,
            "SearchPrice": None,
            "PageIndex": 1,
            "CategoryId": category_id,
            "AppliedBrandIds": None
        })
        response_in_json = api_response.json()
        self.page_number = response_in_json.get("NumPages")

    def data_sender(self, product_instance):
        return Request(self.endpoint_url, body=json.dumps(product_instance), method='POST',
                       headers={'Content-Type': 'application/json'})

    def parse(self, response, **kwargs):
        while self.category < 119:
            self.page_number_saver(self.category)
            pages = self.page_number
            for page in range(1, pages+1):
                yield self.product_scraper_caller(page_number=page, category_id=self.category)
            self.category += 1

    def product_scraper(self, response):
        response_in_json = json.loads(response.body)
        products = response_in_json.get("Products")
        for product in products:
            product_instance = {}
            product_instance['id'] = product['ProductId']
            product_instance['name'] = product['FullName']
            product_instance['slug'] = product['Slug']
            product_instance['category_id'] = response_in_json.get("CategoryId")
            product_instance['category_name'] = response_in_json.get("CategoryName")
            product_instance['price'] = int(product['FinalUnitPrice']) * 10
            product_instance['base_price'] = int(product['FinalUnitPrice']) * 10
            product_instance['vendor'] = "tezol"
            product_id = product_instance['id']
            category_id = product_instance['category_id']
            slug = product_instance['slug']
            formatted_request = self.product_details.replace('category_id', str(category_id)).replace('product_id', str(product_id)).replace('slug', str(slug))
            yield Request(formatted_request, callback=self.product_brand_scraper, cb_kwargs=product_instance)

    def product_brand_scraper(self, response, **product_instance):
        details = response.css('div.fullProductInfo.pull-sm-left.pull-xs-none').css('div.item')
        for detail in details:
            brand = detail.xpath('//span[@itemprop="brand"]/text()').get()
            if brand is not None:
                product_instance['brand'] = brand
                yield self.data_sender(product_instance)
