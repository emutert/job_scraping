# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobscrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_id = scrapy.Field()
    job_title = scrapy.Field()
    salary = scrapy.Field()
    url = scrapy.Field()
    job_type = scrapy.Field()
    contact_name = scrapy.Field()
    mail = scrapy.Field()
    tel = scrapy.Field()
    agency = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    job_salary = scrapy.Field()

    pass
