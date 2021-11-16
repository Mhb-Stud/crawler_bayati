import scrapy


class DrinkSpider(scrapy.Spider):
    name = 'drink'
    my_urls = []
    num_of_pages = 7
    for i in range(1, num_of_pages+1):
        my_urls.append('https://okala.com/drinks-herbaltea?pageNumber='+str(i))
    start_urls = my_urls

    def parse(self, response, **kwargs):
        drinks = response.css('div.col-lg-3.col-md-4.col-sm-6.p-1')
        print(len(drinks))
        for drink in drinks:
            print(drink.css('h2::name'))
            # yield {
            #     'id': drink.css('')
            #
            #  }
