# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

ROBOTSTXT_OBEY = False

# 请将Cookie替换成你自己的Cookie
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Cookie':'ALF=1574512095; SCF=AnG9nZjkIuqV7JCnpE3hjXP_VqaxJ-GqVhQN0XVpCsgRCl1xNkrF1eACYZl7V-l-6M4r0hWzCCUasJ6gdi4DQpo.; SUB=_2A25wteo6DeRhGeFN6VAU9y3JzjiIHXVQWfZyrDV6PUJbktANLWjlkW1NQEEUUDsPyZdKcH5VSay00OgBYuBJilJc; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFLGs2kTL9c7dy.JNTFIovU5JpX5K-hUgL.FoM0eozfS0efSKB2dJLoIEBLxK.L1KzL1-qLxKML1--LB.qLxK.L1-zLBKnLxK-LB-qL1Kzt; SUHB=0rr7c7llZeYk8m; SSOLoginState=1571920490; MLOGIN=1; _T_WM=47357502427; M_WEIBOCN_PARAMS=luicode%3D20000174'
}

# 当前是单账号，所以下面的 CONCURRENT_REQUESTS 和 DOWNLOAD_DELAY 请不要修改

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 3

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None
}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# MongoDb 配置

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017
DB_NAME = 'Sina'
