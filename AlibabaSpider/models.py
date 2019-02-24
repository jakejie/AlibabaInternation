# -*- coding:utf-8 -*-
from datetime import datetime
from sqlalchemy import Column, String, create_engine, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

try:
    from AlibabaSpider.settings import db_host, db_user, db_pawd, db_name, db_port
except Exception as err:
    try:
        from .settings import db_host, db_user, db_pawd, db_name, db_port
    except Exception as err:
        try:
            from settings import db_host, db_user, db_pawd, db_name, db_port
        except Exception as err:
            print("models.py文件中包导入异常：{}".format(err))
# 创建对象的基类:
Base = declarative_base()


# 阿里巴巴数据表
class AlibabaModel(Base):
    __tablename__ = 'alibaba_all'  # 表的名字
    # 表的结构:数据表的设计中 为了方便存储 没有考虑性能 全部设计的200长度 字符串类型
    id = Column(Integer, unique=True, primary_key=True)  # 主键自增
    link = Column(String(200), )  # 商家主页地址
    telephone = Column(String(64), )  # 商家电话
    mobile_phone = Column(String(200), )  # 商家电话2
    fax = Column(String(200), )  # 传真
    address = Column(String(200), )  # 商家地址
    zip = Column(String(200), )  # 邮编
    country_region = Column(String(200), )  # 国家
    province_state = Column(String(200), )  # 省份
    city = Column(String(200), )  # 城市
    contact_name = Column(String(200), )  # 联系人
    contact_department = Column(String(200), )  # 联系人的职称
    contact_job = Column(String(200), )  # 联系人的岗位
    company_nme = Column(String(200), )  # 公司名
    operational_address = Column(String(200), )  # 联系地址
    website = Column(String(200), )  # 网站
    website_on_alibaba = Column(String(200), )  # 阿里巴巴地址
    keyword = Column(String(200), )  # 关键字
    phone_detail_url = Column(String(512), )  # 获取电话的详情页地址
    add_time = Column(DateTime, default=datetime.now)  # 入库时间


if __name__ == "__main__":
    engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'
                           .format(db_user, db_pawd, db_host, db_port, db_name), max_overflow=500)
    Base.metadata.create_all(engine)
