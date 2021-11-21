import scrapy
import requests


class DrinkSpider(scrapy.Spider):
    # name of our spider
    name = 'drink'
    # how many pages do you want the crawler to get
    num_of_pages = 7
    # don't touch
    counter = 2
    # getting url for first page
    start_urls = ['https://okala.com/drinks-herbaltea']
    # address of our api app that we want to send data to
    request_url = 'http://127.0.0.1:8000/'

    """ 
    crawls the website first finding products by their css tag then 
    extracting all their attributes such as product_id,title,...
    then whe use requests module to sent a post request with the json 
    data extracted to request_url after we are done we find the next
    page url and pass the url to response.follow now it calls the
    parse with next_page url and so on until we hit num of pages
    """
    def parse(self, response, **kwargs):
        drinks = response.css('div.col-lg-3.col-md-4.col-sm-6.p-1')
        list_of_products = []
        for drink in drinks:
            product_id = drink.css('a.product-box_image').attrib['data-productid']
            product_title = drink.css('a.product-box_image').attrib['title']
            product_price = (drink.css('div.product-box_price-value.text-secondary::text').get()).replace(' ', '')
            list_of_products.append({
                "id": int(product_id),
                "title": product_title,
                "price": int(product_price.replace(',', '')),
                "base_price": int(product_price.replace(',', ''))
            })
        r = requests.post(self.request_url, json=list_of_products)
        if DrinkSpider.num_of_pages >= DrinkSpider.counter:
            next_page = "https://okala.com/drinks-herbaltea?pageNumber=" + str(DrinkSpider.counter)
            DrinkSpider.counter = DrinkSpider.counter + 1
            yield response.follow(next_page, callback=self.parse)
