# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MedicinpriserItem(scrapy.Item):
    # define the fields for your item here like:
    article_id = scrapy.Field()
    name = scrapy.Field()
    substance = scrapy.Field()
    size = scrapy.Field()
    size_unit = scrapy.Field()
    form = scrapy.Field()
    kategori = scrapy.Field()
    atc = scrapy.Field()
    aktiv_substans = scrapy.Field()
