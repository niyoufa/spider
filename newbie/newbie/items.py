# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewbieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    href = scrapy.Field()
    source = scrapy.Field()
    account = scrapy.Field()
    # toutiao.share,toutiao.star,
    type = scrapy.Field()
    _id = scrapy.Field()
