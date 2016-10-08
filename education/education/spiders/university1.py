#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import UniversityItem
from education.libs import mongolib

import sys,pdb

university_coll = mongolib.get_coll("university")

#抓取中国高校院校等级相关信息
class University1Spider(Spider):
    name = "university1"
    allowed_domains = ["chinadegrees.cn"]
    start_urls  = ["http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346.shtml",
                            "http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346_2.shtml",
                            "http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346_3.shtml"]

    def parse(self, response):
        sel = Selector(response)
        tbody = sel.xpath("//table[1]/tbody")
        trs = tbody.xpath("tr")

        items = []
        for tr in trs[1:]:
            tds = tr.xpath("td")
            try:
                name = tds[0].xpath("p/span/text()").extract()[0]
            except:
                continue
            query_params = {"name":name}
            university = university_coll.find_one(query_params)
            if university :
                university["type"] = tds[1].xpath("p/span/text()").extract()[0]
                if tds[4].xpath("p/span/text()") == []:
                    university["is_211"] = False
                else:
                    university["is_211"] = True

                if tds[5].xpath("p/span/text()") == []:
                    university["is_985"] = False
                else:
                    university["is_985"] = True

                if tds[6].xpath("p/span/text()") == []:
                    university["has_graduate_school"] = False
                else:
                    university["has_graduate_school"] = True
                university_coll.save(university)
        return items



