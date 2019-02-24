# coding:utf-8
import os
import sys
from scrapy import cmdline

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    cmdline.execute(['scrapy', 'crawl', 'alibaba'])
