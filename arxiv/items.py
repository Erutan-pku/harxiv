# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArxivItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    idt      = scrapy.Field()
    url      = scrapy.Field()
    absurl   = scrapy.Field()
    title    = scrapy.Field()
    authors  = scrapy.Field()
    # abstract = scrapy.Field()
    subj     = scrapy.Field()

    # optional fields
    desc     = scrapy.Field()
    jourref  = scrapy.Field()
    




