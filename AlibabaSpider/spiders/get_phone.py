# -*- coding:utf-8 -*-
"""
__author__ = "jake"
__email__ = "jakejie@163.com"
FileName = get_phone.py
site: 
version: python3.6
CreateDay:2018/9/24 11:39
"""
import scrapy

from AlibabaSpider.pipelines import AlibabaspiderPipeline
# try:
#     from AlibabaSpider.pipelines import AlibabaspiderPipeline
# except Exception as e:
#     try:
#         from pipelines import AlibabaspiderPipeline
#     except Exception as e:
#         try:
#             from .pipelines import AlibabaspiderPipeline
#         except Exception as e:
#             print("get_phone.py文件中模块导入异常：{}".format(e))


class CrawlPhone(scrapy.Spider):
    name = 'alibaba_phone'  # scrapy项目名称
    allowed_domains = ['alibaba.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }

    def start_requests(self):
        pass

if __name__ == "__main__":
    pass
