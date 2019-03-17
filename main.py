# -*- coding:utf-8 -*-
#  author: yukun
import time
from multiprocessing import Pool
from spider import parse_link
from indexspider import parse_index

# 目录解析，换成制定的职业,增加城市列表，根据城市来做分析

def main(data):
    url = data['url']
    print(url)
    mongo_table = data['name']
    # 数据库表名不能以.开头
    if mongo_table[0] == '.':
        mongo_table = mongo_table[1:]
    parse_link(url, mongo_table)


if __name__ == '__main__':
    time_start = time.time()
    # 进程池
    pool = Pool(processes=4)
    datas = (data for data in parse_index())
    pool.map(main, datas)
    pool.close()
    # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
    pool.join()

    print('运行时间：',time.time() - time_start)
