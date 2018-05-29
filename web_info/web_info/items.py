# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WebInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    university = scrapy.Field() # 学校
    major = scrapy.Field() #专业
    subject = scrapy.Field() #科目
    sub_symbol = scrapy.Field() #科目代码


