# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: baidu.py 
@time: 2017/11/13 11:23

"""

from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.conf import settings

from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.baidu import ApkInfoItem
from ApkSpider.utils import normalize_and_dup, same_domain


class BaiduSpider(RedisSpider):
    name = 'baidu_spider_redis'
    redis_key = 'baidu_spider:start_urls'
    domain = 'https://shouji.baidu.com'

    def __init__(self, *args, **kwargs):
        super(BaiduSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        if response.url.endswith('.html'):
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('baidu', 0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//span[@class="download-num"]/text()')
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="nav"]/span[5]/a[@target="_self"]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="area-one-setup"]/span/@data_name')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="area-one-setup"]/span/@data_versionname')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="area-one-setup"]/span/@data_package')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//div[@class="area-one-setup"]/span/@data_url')
            yield item_loader.load_item()

        sel = Selector(response)
        links = sel.xpath('//a/@href').extract()
        urls = normalize_and_dup(self.domain, links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
