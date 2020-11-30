import xlwt
from lxml import etree
import requests
import time
import random

import re
import io
import time
import base64
from fontTools.ttLib import TTFont


all_info_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


def get_info(url):
    res = requests.get(url, headers=headers)
    page_content = res.text
    selector = etree.HTML(page_content)

    infos = selector.xpath('//*[@id="list-content"]/div')
    for info in infos[1:]:
        title = info.xpath('div[1]/h3/a/text()')[0].strip()
        yangshi = info.xpath('div[1]/p[1]/text()')[0]
        mianji = info.xpath('div[2]/p[1]/strong/text()')[0]
        info_list = [title, yangshi, mianji]
        all_info_list.append(info_list)

    time.sleep(1)


if __name__ == '__main__':
    urls = [
        'https://shanghai.anjuke.com/community/p{}'.format(str(i)) for i in range(1, 51)]
    for url in urls:
        get_info(url)

    header = ['', '小区', '竣工日期', '二手房均价']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])

    i = 1  # 行
    k = 1  # 序号
    for list in all_info_list:  # 行数据
        j = 1  # 列
        sheet.write(i, 0, k)
        k += 1
        for data in list:  # 列数据
            sheet.write(i, j, data)
            j += 1
        i += 1

    book.save('anjuke_xiaoqu.xls')
