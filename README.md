# 阿里巴巴国际站 商家数据爬虫

## 目标
    阿里巴巴国际站 获取尽可能多的商家数据/含电话号码

## 爬虫原理说明
    根据城市 作为搜索关键字 通过搜索结果 获取商家
    其中，city_list.py文件中有1836个城市 获取有效数据约4万条
    备注：
        由于查看商家电话时，需要用户登录状态或携带cookie信息 因为商家列表与电话号码是分开获取的
        具体获取商家电话号码的方法不予以公开 提供商家数据下载
## 爬虫配置
    1.CONCURRENT_REQUESTS = 200 并发请求数
    2.DOWNLOAD_DELAY = 3 下载延时
    3.CONCURRENT_REQUESTS_PER_DOMAIN = 16 
    4.CONCURRENT_REQUESTS_PER_IP = 16
    5.db_host = '****'  数据库主机
    6.db_user = 'root'  数据库连接用户名
    7.db_pawd = '****'  数据库连接密码
    8.db_name = 'alibaba'  数据库名称
    9.db_port = 3306  数据库端口号
    # 代理ip相关配置
    10.proxy_secret = "**"  讯代理 密钥
    11.proxy_address = "forward.xdaili.cn:80"  # 讯代理 地址
    12.proxy_order_no = "***"   讯代理 订单号
    
## 环境部署
    ubuntu 16 服务器
    1.python环境 
        ubuntu自带python3环境，新服务器需要安装pip virtualenv等相关包
    2.创建虚拟环境
        在项目文件夹中 执行 virtualenv -p python3 env 即可创建虚拟环境
    3.安装依赖库
        激活虚拟环境 执行 source env/bin/activate 即可进入虚拟环境
        安装依赖：pip install -r requests.txt等待安装
        

## 爬虫启动
    1.创建数据表
        在models.py文件下，执行 python models.py 创建数据表
    2.启动爬虫
        在start_alibaba.py文件下 执行 python start_alibaba.py 开启爬虫