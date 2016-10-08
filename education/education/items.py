# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SubjectsItem(scrapy.Item):

    _id = scrapy.Field()

    #学科门类
    category= scrapy.Field()

    #一级学科
    first_level = scrapy.Field()

    #二级学科
    second_level = scrapy.Field()

class UniversityItem(scrapy.Item):

    _id = scrapy.Field()

    # university spider
    #学校名称
    name = scrapy.Field()

    #主管部门
    department = scrapy.Field()

    #所在地
    city = scrapy.Field()

    #办学层次
    level = scrapy.Field()

    # university1 spider 中国高校院校等级
    #类别
    type = scrapy.Field()

    #是否是211
    is_211 = scrapy.Field()

    #是否是985
    is_985 = scrapy.Field()

    # 是否拥有研究生院
    has_graduate_school = scrapy.Field()

    #university2 spider 高校本科招生信息网站
    undergraduate_url = scrapy.Field()



