# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZhihuuserPipeline(object):
    def process_item(self, item, spider):
        return item

class MongodbPipeline(object):
    def __init__(self,mongodb_url,mongo_db):
        self.mongodb_url=mongodb_url
        self.mongo_db=mongo_db
    #def process_item(self, item, spider):
    #   return item
    @classmethod
    def from_crawler(cls,crawler):
        '''
        cls:当前类对象
        :param crawler: 项目组件配置信息
        :return:
        '''
        return cls(
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongodb_url=crawler.settings.get('MONGODB_URL')
        )
    def open_spider(self,spider):
        '''
        在Spider开启时被调用
        :param spider:
        :return:
        '''
        self.client = pymongo.MongoClient(self.mongodb_url)
        self.db = self.client[self.mongo_db]
    def process_item(self,item,item_spider):
        name = item.__class__.__name__
        self.db[name].update({'url_token':item['url_token']},{'$set':item},True)
        #self.db[name].insert(dict(item))
        print('保存成功')
        return item
    def close_item(self,spider):
        '''
        在spider结束时被调用
        :param spider:
        :return:
        '''
        self.client.close()
