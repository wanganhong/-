# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: wandoujia.py 
@time: 2017/11/13 11:30

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.wandoujia import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class WandoujiaSpider(RedisSpider):
    name = 'wandoujia_spider_redis'
    redis_key = 'wandoujia_spider:start_urls'
    domain = 'http://www.wandoujia.com'

    def __init__(self, *args, **kwargs):
        super(WandoujiaSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.startswith('{}/apps/'.format(self.domain)):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('wandoujia',0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//div[@class="num-list"]/span/i/@content')
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="infos"]/dl/dd[2]/a[1]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="app-info"]/p[@class="app-name"]/span/text()')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="infos"]/dl/dd[5]/text()')
            # # 包名
            item_loader.add_value('app_package', response.url.split('apps/')[1])
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="qr-info"]/a/@href')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain) and url.find('/binding') == -1:
                yield Request(url, callback=self.parse)
