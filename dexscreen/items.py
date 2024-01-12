# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DexscreenItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    token = scrapy.Field()
    name = scrapy.Field()
    TRNC = scrapy.Field()
    Volume = scrapy.Field()
    FDV = scrapy.Field()
    Liquidity = scrapy.Field()
    Link = scrapy.Field()
    chain = scrapy.Field()

    



