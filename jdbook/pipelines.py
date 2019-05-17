# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

client = MongoClient()
collections = client["jd"]["book"]

class JdbookPipeline(object):
    def process_item(self, item, spider):
        item["book_name"] =item["book_name"].strip()
        print(item)
        # 将爬取到的数据保存在数据库中
        collections.insert_one(dict(item))
        return item
