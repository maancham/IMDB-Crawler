# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo


class FirstPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['myfilms']
        self.collection = db['films_extra']

    def process_item(self, item, spider):
        if spider.name in ['films_extra']:
            self.collection.insert(dict(item))
            return item
        else:
            return item

class SecondPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['myfilms']
        self.collection = db['ratings']

    def process_item(self, item, spider):
        if spider.name in ['ratings']:
            self.collection.insert(dict(item))
            return item
        else:
            return  item


class ThirdPipeline(object):

    def __init__(self):
        self.conn = pymongo.MongoClient(
            'localhost',
            27017
        )
        db = self.conn['myfilms']
        self.collection = db['reviews']

    def process_item(self, item, spider):
        if spider.name in ['reviews']:
            self.collection.insert(dict(item))
            return item
        else:
            return  item