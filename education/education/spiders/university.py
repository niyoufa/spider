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

#抓取中国高校本科招生网站链接
i = 0
class University2Spider(Spider):
    name = "university2"
    allowed_domains = ["gk114.com"]
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
        sel = Selector(response)
        lis = sel.xpath("//ul/li")
        items = []
        for li in lis:
            try:
                name = li.xpath("a/font/text()").extract()[0]
            except:
                name = li.xpath("a/text()").extract()[0]

            undergraduate_url = li.xpath("a/@href").extract()[0]
            query_params = {
                "name":name,
            }
            university = university_coll.find_one(query_params)
            if university:
                university["undergraduate_url"] = undergraduate_url
                university_coll.save(university)

            print name,undergraduate_url



