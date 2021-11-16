import scrapy


class DrinkSpider(scrapy.Spider):
    name = 'drink'
    start_urls = ['https://okala.com/drinks-herbaltea?pageNumber=7']

    def parse(self, response, **kwargs):
        drinks = response.css('div.col-lg-3.col-md-4.col-sm-6.p-1')
        print(len(drinks))
        # for drink in drinks:
        #     yield {
        #
        #     }
