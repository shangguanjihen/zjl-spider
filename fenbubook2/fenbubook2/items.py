# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy import Item, Field

class Fenbubook2Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    d_name = Field()
    x_name = Field()
    book_url = Field()
    book_img = Field()
    book_name = Field()
    author = Field()
    price = Field()
