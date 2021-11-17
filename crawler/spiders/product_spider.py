import scrapy
import requests


class DrinkSpider(scrapy.Spider):
    name = 'drink'
    my_urls = []
    num_of_pages = 7
    for i in range(1, num_of_pages+1):
        my_urls.append('https://okala.com/drinks-herbaltea?pageNumber='+str(i))
    start_urls = my_urls
    request_url = 'http://127.0.0.1:8000/'

    def parse(self, response, **kwargs):
        drinks = response.css('div.col-lg-3.col-md-4.col-sm-6.p-1')
        print(len(drinks))
        for drink in drinks:
            product_id = drink.css('a.product-box_image').attrib['data-productid']
            product_title = drink.css('a.product-box_image').attrib['title']
            product_price = (drink.css('div.product-box_price-value.text-secondary::text').get()).replace(' ', '')
            r = requests.post(self.request_url, json={
                "product_id": int(product_id),
                "product_title": product_title,
                "product_price": int(product_price.replace(',', '')),
                "price_before_discount": int(product_price.replace(',', ''))
            })
