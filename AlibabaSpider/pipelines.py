# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from AlibabaSpider.settings import db_host, db_user, db_pawd, db_name, db_port
from .models import AlibabaModel

# 创建对象的基类:
Base = declarative_base()


# 数据处理中间件 进行数据入库
class AlibabaspiderPipeline(object):
    # 初始化数据库连接
    def __init__(self):  # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'
                               .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
        # 创建DBSession类型:
        db_session = sessionmaker(bind=engine)
        self.session = db_session()

    # 处理数据入库
    def process_item(self, item, spider):
        info = AlibabaModel(
            link=item['link'],
            telephone=item['telephone'],
            mobile_phone=item['mobile_phone'],
            fax=item['fax'],
            address=item['address'],
            zip=item['zip'],
            country_region=item['country_region'],
            province_state=item['province_state'],
            city=item['city'],
            contact_name=item['contact_name'],
            contact_department=item['contact_department'],
            contact_job=item['contact_job'],
            company_nme=item['company_nme'],
            operational_address=item['operational_address'],
            website=item['website'],
            website_on_alibaba=item['website_on_alibaba'],
            keyword=item['keyword'],
            phone_detail_url=item['phone_detail_url'],
            add_time=datetime.datetime.now()
        )
        try:
            self.session.add(info)
            self.session.commit()
        except Exception as e:
            print('插入数据库时出错 异常原因：{} 插入对象：{}'.format(e, item))
            self.session.rollback()
        return item

    # 提取所有商家/去获取电话号码
    def get_all_business(self):
        result = self.session.query(AlibabaModel).all()
        return result
