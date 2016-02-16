from scrapy.spiders import Spider
from scrapy.selector import Selector 

from tagCrawler.items import TagcrawlerItem

import pdb 

class TutorialSpider(Spider) : 
	name = "tag_spider"
	allowed_domains = ["csdn.net"]
	start_urls = [
		"http://www.csdn.net/tag/",
	]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath("//div[@class='main clearfix tag_list']")
		items = []
		for site in sites : 
		 	tag_info_list = site.xpath("//li/div/div/a")
		 	for tag_info in tag_info_list : 
		 		item = TagcrawlerItem()
		 		item["tag"] = {}
		 		item["tag"]["name"] = tag_info.xpath("text()").extract()[0]
		 		item["tag"]["href"] = tag_info.xpath("@href").extract()[0]
		 		items.append(item)
		return items 
