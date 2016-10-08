#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import UniversityItem
from education.libs import mongolib

import sys,pdb

university_coll = mongolib.get_coll("university")

#抓取中国高校本科招生网站链接
class University2Spider(Spider):
    name = "university2"
    allowed_domains = ["*"]
    start_urls  = ["http://www.gk114.com/"]

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath("/html/body/table[12]/tr/td[1]/table/tr/td/table/tr[2]/td/table/tr")

        new_urls = []
        for tr in trs:
            tds = tr.xpath("td")
            for td in tds:
                new_url = "http://www.gk114.com/" + td.xpath("a/@href").extract()[0]
                new_urls.append(new_url)

        print new_urls
        for new_url in new_urls:
            yield Request(url=new_url, callback=self.parse_post)

    def parse_post(self, response):
        pdb.set_trace()
        sel = Selector(response)
        lis = sel.xpath("//ul/li")
        items = []
        return items




