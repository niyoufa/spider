#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import UniversityItem
from education.libs import mongolib

import sys,pdb

university_coll = mongolib.get_coll("university")

#抓取中国高校名单
class UniversitySpider(Spider):
    name = "university"
    allowed_domains = ["*"]
    start_urls  = ["http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/qgptgxmd/qgptgxmd.html"] #普通高校名单（截至2013年6月21日）

    def parse(self, response):
        sel = Selector(response)
        tbody = sel.xpath("//table[1]/tbody")
        trs = tbody.xpath("tr")

        items = []
        for tr in trs[3:]:
            tds = tr.xpath("td")
            if len(tds) == 1:
                print tds[0].xpath("strong/text()").extract()[0]
            else:
                item = UniversityItem()
                item["name"] = tds[1].xpath("text()").extract()[0]
                item["department"] = tds[2].xpath("text()").extract()[0]
                item["city"] = tds[3].xpath("text()").extract()[0]
                item["level"] = tds[4].xpath("text()").extract()[0]
                query_params = {"name":item["name"]}
                if not university_coll.find_one(query_params):
                    university_coll.save(item)
                else:
                    university_coll.update(query_params,item)
                items.append(item)
        return items



