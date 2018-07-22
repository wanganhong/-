# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: pp.py 
@time: 2017/11/13 15:49

"""

import scrapy
from scrapy.loader.processors import MapCompose

from ApkSpider.utils import statistical_dl_count


def split_pkg(value):
    return value.split(';')[1].split('=')[1]


def split_dl_count(value):
    return statistical_dl_count(value.split('|')[0].strip()[0:-2].replace(' ', ''))


class ApkInfoItem(scrapy.Item):
    task_id = scrapy.Field()
    app_refer_url = scrapy.Field()
    app_dl_count = scrapy.Field(
        input_processor=MapCompose(split_dl_count),
    )
    app_name = scrapy.Field()
    app_category = scrapy.Field()
    app_version = scrapy.Field()
    app_package = scrapy.Field(
        input_processor=MapCompose(split_pkg),
    )
    app_dl_url = scrapy.Field()
    app_dl_url_hash = scrapy.Field()
