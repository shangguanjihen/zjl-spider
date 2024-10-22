# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisSpider
from copy import deepcopy
#from items import Fenbubook2Item
from scrapy_splash import SplashRequest


class WenxuanSpider(RedisSpider):

    name = 'wenxuan'
    allowed_domains = ['www.wenxuan.com','www.winxuan.com','search.winxuan.com','list.winxuan.com','item.winxuan.com']
    redis_key = 'Wenxuan'

    def parse(self, response):
        # 获取大分类列表
        dls = response.xpath('//div[contains(@class,"grid-lt210m0")]//d'
                             'iv[contains(@class,"col-left")]//div[@class="cont"]/dl')
        for dl in dls[1:-3]:
            item = {}
            item['d_name'] = dl.xpath('./dt//text()').extract_first()
            # 获取小分类列表
            dds = dl.xpath('./dd/a')
            for dd in dds:
                x_url = dd.xpath('./@href').extract_first()
                if not x_url == 'http://www.winxuan.com/cms/2017zk':
                    item['x_name'] = dd.xpath('./text()').extract_first()
                    if x_url:
                        #print(x_url)
                        yield scrapy.Request(url=x_url, callback=self.parse_detail, meta={'item': deepcopy(item)})
    def parse_detail(self,response):

        item = response.request.meta['item']
        #print(item)
        book_urls = response.xpath('//*[@id="grid"]/li/ul/li/div/div[1]/a/@href').extract()
        #print(book_urls)

        next = response.xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div[3]/div/a[10]/@href').extract_first()

        for book_url in book_urls:
            item['book_url'] = book_url
            item['book_img'] = response.xpath('//*[@id="grid"]/li[1]/ul/li[1]/div/div[1]/a/img/@src').extract_first()
            if not item['book_img'][:4] == 'http':
                item['book_img'] = 'http:' + item['book_img']
           #yield SplashRequest(url=item['book_url'], callback=self.parse_book_detail, args={'wait': 10},meta={'item': item})
            #print(item)
            yield scrapy.Request(url=book_url,callback=self.parse_book_detail,meta={'item':deepcopy(item)},dont_filter=True)
        if not next == 'javascript:;' and next:
            if not next[:4] == 'http':
                next = 'http:' + next
            yield scrapy.Request(url=next,callback=self.parse_detail,meta={'item':deepcopy(item)},dont_filter=True)
    def parse_book_detail(self, response):

        item3 = response.request.meta['item']  # //*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[2]/dd/b/
        # print(response.text)
        #print(response.body)
        #print(item3)
        item3['book_name'] = response.xpath(
            '//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[1]/h1//text()').extract_first()
        item3['author'] = response.xpath(
            '//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[4]/dd/a/text()').extract()
        item3['price'] = response.xpath(
            '//*[@id="page"]/div[3]/div[1]/div/div[1]/div/div/div[1]/div[2]/dl[2]/dd/b/text()').extract_first()
        #print(item3)
        yield item3