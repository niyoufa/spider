# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SharesItem(scrapy.Item):
    title = scrapy.Field()
    href = scrapy.Field()
    source = scrapy.Field()
    account = scrapy.Field()
    type = scrapy.Field()
    _id = scrapy.Field()

class SubjectsItem(scrapy.Item):
    account = scrapy.Field()
    name = scrapy.Field()
    count = scrapy.Field()
    sub_count = scrapy.Field()
    url = scrapy.Field()
    _id = scrapy.Field()