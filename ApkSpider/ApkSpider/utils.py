# -*- coding:utf-8 -*-  

""" 
@author:CrackM5
@file: utils.py 
@time: 2017/11/08 11:50
"""

import hashlib
from urlparse import urldefrag, urljoin, urlparse


# 链接补全并去重
def normalize_and_dup(base, links):
    urls = set()
    for link in links:
        url = normalize(base, link.strip())
        urls.add(url)
    return urls


# 补全链接
def normalize(base, link):
    link = link.replace('..', '') if link.startswith('..') else link
    # remove hash to avoid duplicates
    link, _ = urldefrag(link)
    return urljoin(base, link)


# 判断url是否和要爬取的网页同域名
def same_domain(url1, url2):
    return urlparse(url1).netloc == urlparse(url2).netloc


# 计算下载量
def statistical_dl_count(string):
    try:
        if string.endswith(u'千'):
            count = float(string[0:-1]) * 1000
        elif string.endswith(u'万'):
            count = float(string[0:-1]) * 10000
        elif string.endswith(u'亿'):
            count = float(string[0:-1]) * 10000 * 10000
        else:
            count = float(string)
    except ValueError:
        count = 0
    return count / 1000


# 获取字符串的MD5哈希值
def get_hash(string):
    md5 = hashlib.md5()
    md5.update(string.encode('utf-8'))
    return md5.hexdigest()