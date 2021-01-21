import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from itemloaders import ItemLoader
from kartishok.items import Article


class KartiSpider(scrapy.Spider):
    name = 'karti'
    allowed_domains = ['kartishok.com']
    start_urls = ['http://kartishok.com/']

    def parse(self, response):
        pass
