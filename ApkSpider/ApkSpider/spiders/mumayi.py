# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: mumayi.py 
@time: 2017/12/14 15:08

"""
import re

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy_redis.spiders import RedisSpider
from scrapy.conf import settings

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.mumayi import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class MumayiSpider(RedisSpider):
    name = 'mumayi_spider_redis'
    redis_key = 'mumayi_spider:start_urls'
    domain = 'http://www.mumayi.com'

    def __init__(self, *args, **kwargs):
        super(MumayiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if re.findall(r'{}/android-\d+.html'.format(self.domain), response.url):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('mumayi', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_value('app_dl_count', 0)
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="place10 fl hidden sb_w"]/a[3]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="place10 fl hidden sb_w"]/span/text()')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="place10 fl hidden sb_w"]/span/text()')
            # 包名
            item_loader.add_xpath('app_package', '//ul[@class="author"]/li[2]/text()')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//a[@id="downurl"]/@href')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a[not(@class="download")]/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain) and url.find('/android') != -1:
                yield Request(url, callback=self.parse)
