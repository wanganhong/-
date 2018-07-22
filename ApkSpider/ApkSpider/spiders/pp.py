# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: pp.py 
@time: 2017/11/13 11:23

"""

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.conf import settings
from scrapy_redis.spiders import RedisSpider

from ApkSpider.items.apk_info_loader import ApkInfoLoader
from ApkSpider.items.pp import ApkInfoItem
from ApkSpider.utils import same_domain, normalize_and_dup


class AnZhiSpider(RedisSpider):
    name = "pp_spider_redis"
    redis_key = "pp_spider:start_urls"
    domain = "https://www.25pp.com"

    def __init__(self, *args, **kwargs):
        super(AnZhiSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        sel = Selector(response)
        if response.url.find('detail_') != -1:
            item_loader = ApkInfoLoader(item=ApkInfoItem(), response=response)
            item_loader.add_value('task_id', settings['SPIDER_TASK'].get('pp',0))
            item_loader.add_value('app_refer_url', response.url)
            # 下载量
            item_loader.add_xpath('app_dl_count', '//div[@class="app-downs"]/text()')
            # 应用名
            item_loader.add_xpath('app_name', '//div[@class="app-title ellipsis"]/text()')
            # 应用类型
            item_loader.add_xpath('app_category', '//div[@class="crumb"]/a[2]/text()')
            # 版本
            item_loader.add_xpath('app_version', '//div[@class="app-detail-info"]/p[2]/span[1]/strong/text()')
            # 包名
            item_loader.add_xpath('app_package', '//div[@class="detail-side"]/@data-stat-exp')
            # 下载地址
            item_loader.add_xpath('app_dl_url', '//a[@class="btn-install large-btn"]/@appdownurl')
            yield item_loader.load_item()

        links = sel.xpath('//a/@href').extract()
        select_links = [link for link in links if link.find('android') != -1]
        urls = normalize_and_dup(self.domain, select_links)
        for url in urls:
            if same_domain(url, self.domain):
                yield Request(url, callback=self.parse)
