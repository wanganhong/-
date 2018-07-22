# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: huawei.py 
@time: 2017/11/13 15:58

"""

import scrapy
from scrapy.loader.processors import MapCompose

from ApkSpider.utils import statistical_dl_count


def split_pkg(value):
    return '.'.join(value.split('/')[-1].split('?')[0].split('.')[:-2])


def split_dl_url(value):
    return value.split(',')[-2].replace('\'', '').strip()


def split_dl_count(value):
    return statistical_dl_count(value.split(u'：')[1][0:-1].strip())


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
    app_dl_url = scrapy.Field(
        input_processor=MapCompose(split_dl_url),
    )
    app_dl_url_hash = scrapy.Field()
