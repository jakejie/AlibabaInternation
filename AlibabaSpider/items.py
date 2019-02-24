# -*- coding: utf-8 -*-
import scrapy


# 获取的字段 定义/每个字段名称 参考models.py文件
class AlibabaspiderItem(scrapy.Item):
    link = scrapy.Field()
    telephone = scrapy.Field()
    mobile_phone = scrapy.Field()
    fax = scrapy.Field()
    address = scrapy.Field()
    zip = scrapy.Field()
    country_region = scrapy.Field()
    province_state = scrapy.Field()
    city = scrapy.Field()
    contact_name = scrapy.Field()
    contact_department = scrapy.Field()
    contact_job = scrapy.Field()
    company_nme = scrapy.Field()
    operational_address = scrapy.Field()
    website = scrapy.Field()
    website_on_alibaba = scrapy.Field()
    keyword = scrapy.Field()
    phone_detail_url = scrapy.Field()
