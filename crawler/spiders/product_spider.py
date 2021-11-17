import scrapy
import requests
import time


class DrinkSpider(scrapy.Spider):
    name = 'drink'
    num_of_pages = 7
    counter = 2
    start_urls = ['https://okala.com/drinks-herbaltea']
    request_url = 'http://127.0.0.1:8000/'

    def parse(self, response, **kwargs):
        drinks = response.css('div.col-lg-3.col-md-4.col-sm-6.p-1')
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
        if DrinkSpider.num_of_pages >= DrinkSpider.counter:
            clicks = response.css('a.page-link')
            next_page = "https://okala.com/drinks-herbaltea?pageNumber=" + str(DrinkSpider.counter)
            DrinkSpider.counter = DrinkSpider.counter + 1
            yield response.follow(next_page, callback=self.parse)
