# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Main_page(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    point = scrapy.Field()
    point_volume = scrapy.Field()
    date = scrapy.Field()
    director = scrapy.Field()
    writer = scrapy.Field()
    cast = scrapy.Field()
    budget = scrapy.Field()
    users = scrapy.Field()
    genres = scrapy.Field()
    gross = scrapy.Field()
    # pass


class Rating_page(scrapy.Item):
    name = scrapy.Field()
    chart = scrapy.Field()
    detail = scrapy.Field()
    extra = scrapy.Field()
    # pass



class Review_page(scrapy.Item):
    data = scrapy.Field()
    name = scrapy.Field()
    # pass
