# -*- coding:utf-8 -*-
#  author: yukun
import requests
import pymongo
from config import *
from bs4 import BeautifulSoup

client = pymongo.MongoClient(MONGO_URL, 27017)
db = client[MONGO_DB]

headers  = {#Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551402322,1552010695,1552571381,1552816228
    'Cookie':'user_trace_token=20190317183124-d051f55e-489f-11e9-9dc8-525400f775ce; LGUID=20190317183124-d051f84e-489f-11e9-9dc8-525400f775ce; JSESSIONID=ABAAABAAAIAACBICE33F6C75FED9EC954F6845B05B35F15; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; _ga=GA1.2.621257881.1552818686; X_HTTP_TOKEN=3876430f68ebc0ae0b8fac6c9f163d45; _ga=GA1.2.621257881.1552818686; LGSID=20190317183124-d051f6b8-489f-11e9-9dc8-525400f775ce; LGRID=20190317183124-d051f7fd-489f-11e9-9dc8-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1551402322; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1552818686',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}


def parse_link(url, MONGO_TABLE):
    for page in range(1, 31):
        link = '{}{}/?filterOption=3'.format(url, str(page))
        resp = requests.get(link, headers=headers)
        if resp.status_code == 404:
            pass
        else:
            soup = BeautifulSoup(resp.text, 'lxml')

            positions = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > h3')
            adds = soup.select('ul > li > div.list_item_top > div.position > div.p_top > a > span > em')
            publishs = soup.select('ul > li > div.list_item_top > div.position > div.p_top > span')
            moneys = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div > span')
            needs = soup.select('ul > li > div.list_item_top > div.position > div.p_bot > div')
            companys = soup.select('ul > li > div.list_item_top > div.company > div.company_name > a')
            tags = []
            if soup.find('div', class_='li_b_l'):
                tags = soup.select('ul > li > div.list_item_bot > div.li_b_l')
            fulis = soup.select('ul > li > div.list_item_bot > div.li_b_r')

            for position,add,publish,money,need,company,tag,fuli in \
					zip(positions,adds,publishs,moneys,needs,companys,tags,fulis):
                data = {
                    'position' : position.get_text(),
                    'add' : add.get_text(),
                    'publish' : publish.get_text(),
                    'money' : money.get_text(),
                    'need' : need.get_text().split('\n')[2],
                    'company' : company.get_text(),
                    'tag' : tag.get_text().replace('\n','-'),
                    'fuli' : fuli.get_text()
                }
                save_database(data, MONGO_TABLE)

def save_database(data, MONGO_TABLE):
    if db[MONGO_TABLE].insert_one(data):
        print('保存数据库成功', data)
