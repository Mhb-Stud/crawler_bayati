import scrapy


class DrinkSpider(scrapy.Spider):
    name = 'drink crawler'
    start_urls = ['https://okala.com/drinks-herbaltea']

    def parse(self, response, **kwargs):
        pass
