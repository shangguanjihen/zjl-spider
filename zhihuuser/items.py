# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    url_token = scrapy.Field()
    follower_count = scrapy.Field()
    articles_count = scrapy.Field()
    answer_count = scrapy.Field()
# class followsItem(scrapy.Item):
#     url_token = scrapy.Field()
#     is_end = scrapy.Field()
#     next = scrapy.Field()
