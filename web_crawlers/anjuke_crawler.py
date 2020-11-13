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


def base64_decode(page_content):
    """
        对base64加密的页面内容进行解密
    """
    # 1、提取出字体文件内容
    base64_str = re.findall("charset=utf-8;base64,(.*?)'\)", page_content)[0]
    font_content = base64.b64decode(base64_str)
    font = TTFont(io.BytesIO(font_content))

    # 2、获取文本对照的字典
    keys = font.getBestCmap()
    keys = {hex(k)[2:]: str(int(v[-2:]) - 1) for k, v in keys.items()}

    # 3、替换文本内容
    for k, v in keys.items():
        page_content = page_content.replace(f'&#x{k};', v)
    return page_content


all_info_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


def get_info(url):
    res = requests.get(url, headers=headers)
    page_content = base64_decode(res.text)
    selector = etree.HTML(page_content)

    infos = selector.xpath('//*[@id="list-content"]/div')
    for info in infos[2:]:
        title = info.xpath('div[1]/h3/a/b/text()')[0].strip()
        yangshi = info.xpath('div[1]/p[1]/b[1]/text()')[0]
        mianji = info.xpath('div[1]/p[1]/b[2]/text()')[0]
        niandai = info.xpath('div[1]/p[1]/b[3]/text()')
        dizhi = info.xpath('div[1]/address/a/text()')[0].strip()
        danjia = info.xpath('div[1]/p[1]/text()')[4]
        zongjia1 = info.xpath('div[2]/p/strong/b/text()')
        zongjia = zongjia1
        biaoqians = info.xpath('div[1]/p[2]/span')
        t = ''
        for biaoqian in biaoqians:
            t += (biaoqian.xpath('text()')[0])
        dizhi1 = info.xpath('div[1]/address/text()')
        info_list = [title, yangshi, mianji, niandai,
                     dizhi, danjia, zongjia, t, dizhi1]
        all_info_list.append(info_list)

    time.sleep(1)


if __name__ == '__main__':
    urls = [
        'https://sh.zu.anjuke.com/fangyuan/px2-x1-p{}'.format(str(i)) for i in range(1, 51)]
    for url in urls:
        get_info(url)

    header = ['序号', '标题', '室', '厅', '平米', '小区', '楼层', '价格', '标签', '地址']
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

    book.save('anjuke_fake2.xls')
