# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DataconsumptionItem(scrapy.Item):
    # define the fields for your item here like:
    total = scrapy.Field()
    download = scrapy.Field()
    upload = scrapy.Field()
    remaining = scrapy.Field()
    date = scrapy.Field()
    dl_pct = scrapy.Field()
    ul_pct = scrapy.Field()

    dl = scrapy.Field()