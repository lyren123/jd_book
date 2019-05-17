# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdbookItem(scrapy.Item):
    # define the fields for your item here like:
    cate = scrapy.Field()
    s_cate = scrapy.Field()
    cate_href = scrapy.Field()
    book_href = scrapy.Field()
    book_name = scrapy.Field()
    press = scrapy.Field()
    publish_date = scrapy.Field()
    price = scrapy.Field()
