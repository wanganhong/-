# -*- coding:utf-8 -*-  

""" 

@author:CrackM5
@file: seed_add.py 
@time: 2017/11/14 20:02

"""

from redis import Redis

from ApkSpider.settings import REDIS_HOST, REDIS_PORT, REDIS_PARAMS

'''
sadd anzhi_spider:start_urls 'http://www.anzhi.com'
sadd appchina_spider:start_urls 'http://www.appchina.com'
sadd baidu_spider:start_urls 'https://shouji.baidu.com'
sadd huawei_spider:start_urls 'http://appstore.huawei.com'
sadd myapp_spider:start_urls 'http://android.myapp.com'
sadd pp_spider:start_urls 'https://www.25pp.com'
sadd qihu360_spider:start_urls 'http://zhushou.360.cn'
sadd xiaomi_spider:start_urls 'http://app.mi.com'
sadd wandoujia_spider:start_urls 'http://www.wandoujia.com'

'''

SEEDS = {
    'anzhi_spider:start_urls': 'http://www.anzhi.com',
    'appchina_spider:start_urls': 'http://www.appchina.com',
    'baidu_spider:start_urls': 'https://shouji.baidu.com',
    'huawei_spider:start_urls': 'http://appstore.huawei.com',
    'myapp_spider:start_urls': 'http://android.myapp.com',
    'pp_spider:start_urls': 'https://www.25pp.com',
    'qihu360_spider:start_urls': 'http://zhushou.360.cn',
    'xiaomi_spider:start_urls': 'http://app.mi.com',
    'wandoujia_spider:start_urls': 'http://www.wandoujia.com',
    'mumayi_spider:start_urls': 'http://www.mumayi.com',

}

r = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PARAMS['password'], db=REDIS_PARAMS['db'])

for sname, seed in SEEDS.items():
    print 'Add seed:{} to {}'.format(seed, sname)
    r.sadd(sname, seed)
