# -*- coding: utf-8 -*-
import scrapy
import json
from zhihuuser.items import UserItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    #start_urls = ['https://www.zhihu.com/org/wang-yi-kan-ke/followers']

    start_user = 'wang-yi-kan-ke'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include={data}'
    user_data = 'allow_message,is_followed,is_following,is_org,is_blocking,employments,answer_count,follower_count,articles_count,gender,badge[?(type=best_answerer)].topics'


    follower_url = 'https://www.zhihu.com/api/v4/members/{user}/followers?include={include}&offset={offset}&limit={limit}'
    follower_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'

    follows_url = 'https://www.zhihu.com/api/v4/members/{}/followees?include={}&offset={}&limit={}'
    follows_query = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    def start_requests(self):
        #用户信息
        yield scrapy.Request(url=self.user_url.format(user=self.start_user,data=self.user_data),callback=self.parse_user)

        #粉丝
        yield scrapy.Request(url=self.follower_url.format(user=self.start_user,include=self.follower_query,offset=20,limit=20),callback=self.parse_follower)

        #关注的人
        yield scrapy.Request(url=self.follows_url.format(user=self.start_user,include=self.follows_query,offset=20,limit=20),callback=self.parse_follows)

    def parse_user(self, response):
        '''
        获取用户信息
        :param response:
        :return:
        '''
        text=json.loads(response.text)
        item = UserItem()
        for field in item.fields:  #获取所有键值
            if field in text.keys(): #如果键值存在
                item[field] = text.get(field)
        yield item
        yield scrapy.Request(url=self.follower_url.format(user=text.get('url_token'),include=self.follower_query,offset=0,limit=20),callback=self.parse_follows)

    def parse_follows(self, response):
        '''
        获取用户的关注列表
        :param response:
        :return:
        '''
        #print(response.text)
        text = json.loads(response.text)
        if 'data' in text.keys():
            for result in text.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), data=self.user_data),
                                     callback=self.parse_user)
        if 'paging' in text.keys() and  text.get('paging').get('is_end') == False:
            next = text.get('paging').get('next')
            yield scrapy.Request(url=next,callback=self.parse_follows)
    def parse_follower(self, response):
        '''
        获取用户的关注列表
        :param response:
        :return:
        '''
        #print(response.text)
        text = json.loads(response.text)
        if 'data' in text.keys():
            for result in text.get('data'):
                yield scrapy.Request(url=self.user_url.format(user=result.get('url_token'), data=self.user_data),
                                     callback=self.parse_user)
        if 'paging' in text.keys() and  text.get('paging').get('is_end') == False:
            next = text.get('paging').get('next')
            yield scrapy.Request(url=next,callback=self.parse_follower)