# -*- coding: utf-8 -*-
import re
import json
import scrapy
from AlibabaSpider.items import AlibabaspiderItem

try:
    from .city_list import city_list_low
except Exception as e:
    try:
        from AlibabaSpider.spiders.city_list import city_list_low
    except Exception as e:
        print("alibaba.py文件中模块导入异常：{}".format(e))


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'  # scrapy项目名称
    allowed_domains = ['alibaba.com']
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    }

    # 爬虫入口函数
    def start_requests(self):
        for city in city_list_low[:1000]:
            url_s = 'http://www.alibaba.com/trade/search?&keyword={}&viewType=L&indexArea=company_en&page=1&n=50' \
                .format(city[0])
            yield scrapy.Request(url=url_s,
                                 headers=self.headers,
                                 dont_filter=True,
                                 callback=self.parse_list,
                                 meta={"keyword": city[1], }
                                 )

    # 处理列表页
    def parse_list(self, response):
        keyword = response.meta["keyword"]
        href_list = response.xpath("//div[@class='company']/a[@class='cd']/@href").extract()
        for url_detail in href_list:  # 遍历列表结果 访问详情页并提取数据
            yield scrapy.Request(url=url_detail,
                                 headers=self.headers,
                                 dont_filter=True,
                                 callback=self.parse_detail,
                                 meta={"keyword": keyword},
                                 )
        # 下一页
        next_page = "".join(response.xpath('//a[@class="next"]/@href').extract())
        if next_page:
            if 'http' not in next_page:
                next_page = 'http:' + next_page
            yield scrapy.Request(url=next_page,
                                 headers=self.headers,
                                 dont_filter=True,
                                 callback=self.parse_list,
                                 meta={"keyword": keyword},
                                 )

    # 详情主页
    def parse_detail(self, response):
        link = response.url
        city = "".join(response.xpath('//table[@class="info-table"]/tr[last()]/td/text()').extract())
        province_state = "".join(response.xpath('//table[@class="info-table"]/tr[last()-1]/td/text()').extract())
        country_region = "".join(response.xpath('//table[@class="info-table"]/tr[last()-2]/td/text()').extract())
        zip_code = "".join(response.xpath('//table[@class="info-table"]/tr[last()-3]/td/text()').extract())
        if zip_code.isdigit():
            zip_code = zip_code
            address = "".join(response.xpath('//table[@class="info-table"]/tr[last()-4]/td/text()').extract())
        else:
            zip_code = ''
            address = "".join(response.xpath('//table[@class="info-table"]/tr[last()-3]/td/text()').extract())
        company_name = "".join(response.xpath('//table[@class="contact-table"]/tr[1]/td/text()').extract())
        operational_address = "".join(response.xpath('//table[@class="contact-table"]/tr[2]/td/text()').extract())
        website = "".join(response.xpath('//table[@class="contact-table"]/tr[3]/td/div/text()').extract())
        website_on_alibaba = "".join(response.xpath('//table[@class="contact-table"]/tr[last()]/td/a/text()').extract())
        contact_name = "".join(response.xpath('//div[@class="contact-name"]/text()').extract())
        contact_department = "".join(response.xpath('//div[@class="contact-department"]/text()').extract())
        contact_job = "".join(response.xpath('//div[@class="contact-job"]/text()').extract())
        data_dict = {'link': link,
                     'city': city,
                     'province_state': province_state,
                     'country_region': country_region,
                     'zip': zip_code,
                     'address': address,
                     'company_nme': company_name,
                     'operational_address': operational_address,
                     'website': website,
                     'website_on_alibaba': website_on_alibaba,
                     'contact_name': contact_name,
                     'contact_department': contact_department,
                     'contact_job': contact_job, }
        account_id_list = re.findall(re.compile(r'encryptAccountId%22%3A%22(.*?)%'), response.text)
        if account_id_list:
            account_id = account_id_list[0]
            print(account_id)
            host = response.url.split('://')[-1].split('/')[0]
            phone_detail_url = 'http://{}/event/app/contactPerson/showContactInfo.htm?encryptAccountId={}' \
                .format(host, account_id)
        else:
            phone_detail_url = ""
        # if phone_detail_url:
        #     yield scrapy.Request(url=phone_detail_url,
        #                          callback=self.parse_phone_detail,
        #                          headers=self.headers,
        #                          dont_filter=True,
        #                          meta={"data_dict": data_dict}
        #                          )
        items = AlibabaspiderItem()
        items['telephone'] = ""
        items['mobile_phone'] = ""
        items['fax'] = ""
        items['phone_detail_url'] = phone_detail_url
        items['link'] = data_dict['link']
        items['address'] = data_dict['address']
        items['zip'] = data_dict['zip']
        items['country_region'] = data_dict['country_region']
        items['province_state'] = data_dict['province_state']
        items['city'] = data_dict['city']
        items['contact_name'] = data_dict['contact_name']
        items['contact_department'] = data_dict['contact_department']
        items['contact_job'] = data_dict['contact_job']
        items['company_nme'] = data_dict['company_nme']
        items['operational_address'] = data_dict['operational_address']
        items['website'] = data_dict['website']
        items['website_on_alibaba'] = data_dict['website_on_alibaba']
        items['keyword'] = response.meta['keyword']
        yield items

    # 获取到电话号码等隐私信息
    @staticmethod
    def parse_phone_detail(response):
        print("处理获取手机号：{}  内容：{}".format(response.url, response.text))
        phone_data = json.loads(response.text)
        if "contactInfo" in phone_data:
            fax = phone_data["contactInfo"]["accountFax"] if "accountFax" in phone_data["contactInfo"] else ''
            mobile_phone = phone_data["contactInfo"]["accountMobileNo"] if "accountMobileNo" in phone_data[
                "contactInfo"] else ''
            telephone = phone_data["contactInfo"]["accountPhone"] if "accountPhone" in phone_data[
                "contactInfo"] else ''
        else:
            fax = ''
            mobile_phone = ''
            telephone = ''
        items = AlibabaspiderItem()
        items['link'] = response.meta['data_dict']['link']
        items['telephone'] = telephone
        items['mobile_phone'] = mobile_phone
        items['fax'] = fax
        items['address'] = response.meta['data_dict']['address']
        items['zip'] = response.meta['data_dict']['zip']
        items['country_region'] = response.meta['data_dict']['country_region']
        items['province_state'] = response.meta['data_dict']['province_state']
        items['city'] = response.meta['data_dict']['city']
        items['contact_name'] = response.meta['data_dict']['contact_name']
        items['contact_department'] = response.meta['data_dict']['contact_department']
        items['contact_job'] = response.meta['data_dict']['contact_job']
        items['company_nme'] = response.meta['data_dict']['company_nme']
        items['operational_address'] = response.meta['data_dict']['operational_address']
        items['website'] = response.meta['data_dict']['website']
        items['website_on_alibaba'] = response.meta['data_dict']['website_on_alibaba']
        items['keyword'] = response.meta['keyword']
        yield items
