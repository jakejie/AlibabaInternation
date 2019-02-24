# -*- coding: utf-8 -*-
import time
import hashlib
from scrapy import signals
from AlibabaSpider.settings import proxy_secret, proxy_address, proxy_order_no


# 代理中间件 添加代理ip
class ProxyMiddleware(object):
    # 请求之前加上代理
    @staticmethod
    def process_request(request, spider):
        proxy_server = "http://{}".format(proxy_address)
        timestamp = str(int(time.time()))  # 计算时间戳
        md5_string = hashlib.md5(str(
            "orderno={},secret={},timestamp={}".format(proxy_order_no, proxy_secret, timestamp)).encode()).hexdigest()
        proxy_auth = "sign={}&orderno={}&timestamp={}".format(md5_string.upper(), proxy_order_no, timestamp)
        request.meta["proxy"] = proxy_server
        request.headers["Proxy-Authorization"] = proxy_auth

    # 返回response进行检查
    @staticmethod
    def process_response(request, response, spider):
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            print("状态码异常：{}".format(response.status))
            return request
        if response is None:
            print("返回空类型")
            return request
        if len(response.text) == 0:
            print("返回空字符串:Status-->{} Response-->{}".format(response.status, response.text))
            return request
        return response

    # 出现异常的请求
    @staticmethod
    def process_exception(request, exception, spider):
        print("重新处理出现异常的请求")
        return request


class AlibabaspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AlibabaspiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
