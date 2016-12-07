# coding=utf8
from srapy.src import index
import time
# 抓取100页
# 以追加模式来写文件
# 和存入数据库一样的道理,读取完一页过后,需要休眠10秒,为了防止爬虫崩溃,可以一段段获取.
# 写入csv文件已经经过测试,目前是可行的
f_obj = open('data.csv', 'a')
i = 1
while(i < 2):
    url_list = index.getURLs('https://search.jd.com/Search?keyword=%E5%8F%A3%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%8F%A3%E7%BD%A9&page=' + str(i))
    for item in url_list:
        data = index.getItemInfo(item[0], item[1])
        # print(item)
        # csv的格式是: id,title,comment,price,name,weight,origin
        data_toString = data['id']+','+data['title']+','+data['comment']+','+data['price']+','+data['name']+','+data['weight']+','+data['origin']+'\n'
        try:
            f_obj.write(data_toString)
        except:
            print('some_error')
    i += 1
    time.sleep(10)
f_obj.close()
