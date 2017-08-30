# -*- coding: utf-8 -*-

import scrapy
from tutorial.items import TutorialItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class QuotesSpider(CrawlSpider):

    name = 'quotes'
    allowed_domains = ['mzitu.com']
    start_urls = ['http://www.mzitu.com/']
    img_urls = []
    rules = (
        Rule(LinkExtractor(allow=('http://www.mzitu.com/\d{1,6}',), deny=('http://www.mzitu.com/\d{1,6}/\d{1,6}')),
             callback='parse_url', follow=True),
    )

    # def parse_url(self, response):
        # yield scrapy.Request(url=response.url, callback=self.parse_single)

    # def start_requests(self):
    #     urls = [
    #         'http://www.mzitu.com/86048'
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse_url)

    def parse_url(self, response):
        item = TutorialItem()
        info = response.css("div.main")
        max_num = info.css("div.pagenavi").xpath("a/span/text()").extract()[-2]
        name = info.css("h2.main-title::text").extract_first()
        item['name'] = name
        # item['name'] = response.url.split('/')[-1]
        for num in range(1, int(max_num)+1):
            page_url = response.url + "/" + str(num)
            yield scrapy.Request(url=page_url,  meta={'item': item}, callback=self.img_url,dont_filter=True)

    def img_url(self, response):
        item = response.meta['item']
        img_url = response.css('div.main-image').xpath('p/a/img/@src').extract_first()
        # for img in img_urls:
        item['image_url'] = img_url
        yield item