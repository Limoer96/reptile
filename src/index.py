# coding=utf8
from urllib.request import urlopen
from urllib.error import HTTPError
import re
from bs4 import BeautifulSoup
import json


# 该函数用于获取1页的商品链接和其编号
def getURLs(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        # 取得所有的商品项
        items = bsObj.find_all('li', class_='gl-item')
        url_list = []
        for item in items:
            item_url = item.find('a', href=re.compile(r'//item.jd.com/(\d+).html$'))  # 排除那些推广的表项
            if item_url == None:
                continue
            else:
                clear_item = 'https:' + item_url['href']  # 获得url
                id = re.match(r'https://item.jd.com/(\d+).html$', clear_item).groups()[0]  # 获得编号
                url_list.append([clear_item, id])  # 添加编号
    except AssertionError as e:
        return None
    return url_list


# 此函数用于获取价格,因为这里京东做了防爬虫措施,使用的是ajax提交获得价格, 这里使用id单独查询到价格
def getPrice(id):
    price_obj = urlopen('http://p.3.cn/prices/mgets?skuIds=J_' + id)
    price_html = BeautifulSoup(price_obj.read(), 'lxml')
    str = price_html.find('p').contents[0]
    new_str = str[1: -2]
    json_obj = json.loads(new_str)
    price = json_obj['p']
    return price


# 同理,需要单独查询评论数(精确值)
def getComment(id):
    obj = urlopen('http://club.jd.com/productpage/p-' + id + '-s-0-t-3-p-0.html')
    html = BeautifulSoup(obj.read(), 'lxml')
    str_string = html.find('p').contents[0]
    comment = re.match(r'(.*),"commentCount":(\d+)', str_string).groups()[1]
    return comment


# 进入某个url, 取得一些需要的信息并返回
def getItemInfo(url, id):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml')
        # 获取标题
        title = bsObj.find('div', id='name').contents[1].contents[0]
        # 获取商品价格

        price = getPrice(id)
        # 获取商品的粗略评价()
        comment = getComment(id)
        # 获取商品的其他信息
        infos = bsObj.find_all('ul', id='parameter2')[0].contents
        g_name = infos[1].contents[0][5:]
        g_id = id
        g_weight = infos[5].contents[0][5:]
        g_origin = infos[7].contents[0][5:]
        # 这里有些没有产地,做如下处理
        if(re.match(r'.*(\d+).*', g_origin)):
            g_weight = g_origin
            g_origin = ''
        # g_weight = infos[5].contents[0][5:]
        # 到目前为止只能获取: 标题,价格,商品名,编号,重量和产地,尝试获取销量中(没有销量,只有评价数)
    except AssertionError as e:
        return None
    return {
        'title': title,  # 标题
        'price': price,  # 价格
        'comment': comment,  # 评论数
        'name': g_name,  # 商品名
        'id': g_id,  # 编号
        'weight': g_weight,  # 重量
        'origin': g_origin  # 产地
    }


# if __name__ == 'main':
#     # 测试能否取得title
# info = getItemInfo('https://item.jd.com/2582352.html', '2582352')
# print(info)
# print(getPrice('2582352'))
# print(getComment('2582352'))

# list = getURLs('https://search.jd.com/Search?keyword=%E5%8F%A3%E7%BD%A9&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E5%8F%A3%E7%BD%A9&page=1')
# if list == None:
#     print('not find')
# else:
#     print(list)
