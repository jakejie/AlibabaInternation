# -*- coding: utf-8 -*-
BOT_NAME = 'AlibabaSpider'

SPIDER_MODULES = ['AlibabaSpider.spiders']
NEWSPIDER_MODULE = 'AlibabaSpider.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 200
# DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

db_host = '****'
db_user = 'root'
db_pawd = '****'
db_name = 'alibaba'
db_port = 3306

# 代理ip相关配置
proxy_secret = "***"  # 讯代理 密钥
proxy_address = "forward.xdaili.cn:80"
proxy_order_no = "***"  # 讯代理 订单号

ITEM_PIPELINES = {
    'AlibabaSpider.pipelines.AlibabaspiderPipeline': 300,
}
REDIRECT_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 10
RETRY_HTTP_CODECS = [500, 502, 503, 504, 408, 403, 400, 429, 302]
DOWNLOADER_MIDDLEWARES = {
    'AlibabaSpider.middlewares.ProxyMiddleware': 110,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 120,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 130,
}
