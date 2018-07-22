# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: xiaomi.py 
@time: 2017/11/13 11:24

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.xiaomi import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class XiaomiSpider(RedisSpider):
    name = 'xiaomi_spider_redis'
    redis_key = 'xiaomi_spider:start_urls'
    domain = 'http://app.mi.com'

    def __init__(self, *args, **kwargs):
        super(XiaomiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.startswith('{}/details?id='.format(self.domain)):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('xiaomi', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_value('app_dl_count', 0)
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="bread-crumb"]/ul/li[2]/a/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="intro-titles"]/h3/text()')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="details preventDefault"]/ul/li[4]/text()')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="details preventDefault"]/ul/li[8]/text()')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="details preventDefault"]/ul/li[10]/text()')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a[not(@class="download")]/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
