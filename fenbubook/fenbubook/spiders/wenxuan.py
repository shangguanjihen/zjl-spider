# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
from scrapy_splash import SplashRequest
import re
class WenxuanSpider(RedisSpider):
    name = 'wenxuan'
    allowed_domains = ['www.winxuan.com','search.winxuan.com','list.winxuan.com','item.winxuan.com']
    redis_key = 'Wenxuan'
    #start_urls = ['http://www.winxuan.com/']

    def parse(self, response):
        # 获取大分类列表
        dls = response.xpath('//div[contains(@class,"grid-lt210m0")]//d'
                             'iv[contains(@class,"col-left")]//div[@class="cont"]/dl')
        for dl in dls[1:-3]:
            item = {}
            item['d_name'] = dl.xpath('./dt//text()').extract_first()
            #获取小分类列表
            dds = dl.xpath('./dd/a')
            for dd in dds:
                x_url = dd.xpath('./@href').extract_first()
                if not x_url == 'http://www.winxuan.com/cms/2017zk':
                    item['x_name'] = dd.xpath('./text()').extract_first()
                    if x_url:
                        print(x_url)
                        yield scrapy.Request(url=x_url,callback=self.parse_detail,meta={'item':deepcopy(item)})
    def parse_detail(self,response):
        '''
        解析产品列表页面，提取出每个产品链接
        :param response:
        :return:
        '''
        item = response.meta['item']

        # script = '''
        #        function main(splash, args)
        #             splash.images_enabled = false
        #             splash:wait(2)
        #             assert(splash:go(args.url))
        #             assert(splash:wait(0.5))
        #             return splash:html()
        #         end
        #        '''
        book_urls = response.xpath('//*[@id="grid"]/li/ul/li/div/div[1]/a/@href').extract()
        #print(book_urls)
        for book_url in book_urls:
            item['book_url'] = book_url
            item['book_img'] = response.xpath('//*[@id="grid"]/li[1]/ul/li[1]/div/div[1]/a/img/@src').extract_first()
            if not item['book_img'][:4] == 'http':
                item['book_img'] = 'http' + item['book_img']
            yield SplashRequest(url=item['book_url'], callback=self.parse_book_detail, args={'wait':10},meta={'item': item})
            #yield Request(url=item['book_url'],callback=self.parse_book_detail,meta={'item':item})
    def parse_book_detail(self,response):
        item3 = response.meta['item']#//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[2]/dd/b/
        #print(response.text)
        item3['book_name'] = response.xpath('//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1//text()').extract_first()
        item3['author'] = response.xpath('//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[4]/dd/a/text()').extract()
        item3['price'] = response.xpath('//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[2]/dd/b/text()').extract_first()
        item3['intro'] = response.xpath('//*[@id="page"]/div[3]/div[1]/div/div[5]/div/div[5]/div[2]/div/text()').extract_first()
        yield item3