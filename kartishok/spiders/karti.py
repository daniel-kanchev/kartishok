import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from kartishok.items import Article


class KartiSpider(scrapy.Spider):
    name = 'karti'
    allowed_domains = ['kartishok.com']
    start_urls = ['https://www.kartishok.com/']

    def parse(self, response):
        articles = response.xpath('//article')
        for article in articles:
            link = article.xpath(".//a[text()='Прочети още']/@href").get()
            meta = article.xpath(".//div[@class='entry-meta']/ul//text()").getall()

            yield response.follow(link, self.parse_article, cb_kwargs=dict(meta=meta))

        next_page = response.xpath("//a[@class='blog-pager-older-link']/@href").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response, meta):
        item = ItemLoader(Article(), response)
        item.default_output_processor = TakeFirst()

        meta = [text.strip() for text in meta if text.strip()]
        if meta[0].endswith(" г."):
            date = meta.pop(0)
            date = format_date(date[:-3])
        else:
            date = "No Date"

        meta.pop(0)
        meta.pop(-1)

        categories = ", ".join(meta) if meta else "No Categories"

        title = response.xpath("//h1//text()").get()

        content = response.xpath("//div[@class='entry-content']//text()").getall()
        if content:
            content[0] = content[0].strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('categories', categories)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()


def format_date(date):
    date_dict = {
        "януари": "January",
        "февруари": "February",
        "март": "March",
        "април": "April",
        "май": "May",
        "юни": "June",
        "юли": "July",
        "август": "August",
        "септември": "September",
        "октомври": "October",
        "ноември": "November",
        "декември": "December",
    }

    date = date.split(" ")
    for key in date_dict.keys():
        if date[1] == key:
            date[1] = date_dict[key]
    date = " ".join(date)

    date_time_obj = datetime.strptime(date, '%d %B %Y')
    date = date_time_obj.strftime("%Y/%m/%d")

    return date
