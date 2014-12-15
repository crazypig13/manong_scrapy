# -*- coding: utf-8 -*-
import scrapy
from s1.items import S1Item


class ExSpider(scrapy.Spider):
    name = "ex"
    allowed_domains = ["weekly.manong.io"]
    start_urls = (
        'http://weekly.manong.io/issues/',
    )

    def parse(self, response):
        items = []
        for h4 in response.xpath('//h4'):
            url = h4.xpath('a/@href').extract()[0]
            yield scrapy.Request(url, callback=self.parseSingle)

    def parseSingle(self, response):
        index = response.xpath('//h2/text()').extract()[0]

        title = ''
        info = ''
        name = ''
        link = ''
        ready = 0
        for n in response.xpath('//h3|//h4|//p'):
            t = n.xpath('name()').extract()[0]
            if t == 'h3':
                title = n.xpath('text()').extract()[0]
            elif t == 'h4':
                name = n.xpath('a/text()').extract()[0]
                link = n.xpath('a/@href').extract()[0]
                ready = 1
            elif t == 'p' and ready == 1:
                ready = 0
                info = n.xpath('text()').extract()[0]
                item = S1Item()
                item['title'] = title
                item['name'] = name
                item['link'] = link
                item['info'] = info 
                item['index'] = index 
                yield item
        pass
