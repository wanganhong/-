# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: apk_info_loader.py
@time: 2017/11/13 15:40

"""

from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst


class ApkInfoLoader(ItemLoader):
    default_input_processor = MapCompose(lambda s: _strip(s))
    default_output_processor = TakeFirst()


def _strip(_in):
    if type(_in) in (str, unicode):
        return _in.strip()
    return _in
