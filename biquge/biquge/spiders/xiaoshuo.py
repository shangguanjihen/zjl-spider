# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import os
class XiaoshuoSpider(CrawlSpider):
    name = 'xiaoshuo'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['http://www.xbiquge.la/paihangbang/']
    #def start_requests(self):

    rules = (
        #爬取每一个小说链接，将结果返回
        Rule(LinkExtractor(allow=r'http://www.xbiquge.la/\d+/\d+/'),callback='parse_item'),
        #Rule(LinkExtractor(allow=r'/d+/d+/d+\.html'),callback='parse_item'),
    )


    def parse_item(self, response):
        #print(response)
        item = {}
        item['c'] = 1
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        item['name'] = response.xpath('//*[@id="info"]/h1/text()').extract_first()
        item['author'] = response.xpath('//*[@id="info"]/p[1]/text()').extract_first()
        item['time'] = response.xpath('//*[@id="info"]/p[3]/text()').extract_first()
        item['jianjie'] = response.xpath('//*[@id="intro"]/p[2]/text()').extract_first()
        url = response.xpath('//*[@id="list"]/dl/dd/a/@href').extract_first()
        url = 'http://www.xbiquge.la' + url
        yield scrapy.Request(url=url,callback=self.parse_detail,meta={'item':item},dont_filter=True)
        #print(item)
        #return item
    def parse_detail(self, response):
        item = response.meta['item']
        section = response.xpath('//*[@id="wrapper"]//div[@class="bookname"]//h1/text()').extract_first()
        bodys = response.xpath('//*[@id="content"]/text()').extract()
        next = response.xpath('//*[@id="wrapper"]//div[@class="bottem1"]/a[4]/@href').extract_first()
        next = 'http://www.xbiquge.la'+ next
        #print(next)
        text = response.xpath('//*[@id="wrapper"]//div[@class="bottem1"]/a[4]/text()').extract_first()
        #print(body)//*[@id="wrapper"]/div[4]/div/div[2]/div[1]/a[4]
        file_path = '笔趣阁前20名各类小说'
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_name = item['name'] + '.txt'

        with open(file_path + '/'+ file_name,'a') as f:
            if item['c'] == 1:
                f.write(item['name']+'\n')
                f.write(re.sub('\xa0','',item['author'])+'\n')
                f.write(item['time']+'\n')
                f.write(item['jianjie']+'\n'+'\n')
                item['c'] = 0
            f.write(section + '\n')
            for body in bodys:
                f.write(re.sub('[\ufeff \xa0]',' ',body))
            f.write('\n'+'\n')
        if next[-4:] == 'html':
            yield scrapy.Request(url = next,callback = self.parse_detail,meta = { 'item':item},dont_filter = True)
        else:
            yield item
