# coding=utf8
import pymysql
import time
from srapy.src import index
# 我看了一下别说100页,就是20页后就很少有销量了,所以这里只看爬取100页的商品项
# 数据库有配置问题的话(或者是打错了字),请自行修改
# 为了保证程序不崩溃,请分段获取数据,比如先获取10页,再修改i的值再打开获取
# 防止京东对爬虫有所察觉,每次获得一页数据后就sleep 10秒, 实际可以弄得更长些
# 创建连接对象
conn = pymysql.connect(host='127.0.0.1', port=3306, user='izengm11', passwd='', db='izengm11', charset='utf8')
# 创建游标
cursor = conn.cursor()
i = 0
while (i<100):
    url_list = index.getURLs('https://search.jd.com/Search?keyword=%E5%8F%A3%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%8F%A3%E7%BD%A9&page=' + str(i))
    for item in url_list:
        info = index.getItemInfo(item[0], item[1])
        cursor.execute("insert into info(title,price,comment,g_name,id,weight,origin)values(%s,%s,%s,%s,%s,%s,%s)", (info['title'], info['price'], info['comment'], info['name'],info['id'], info['weight'], info['origin']))
        conn.commit()
    i += 1
    time.sleep(10)
cursor.close()
conn.close()

