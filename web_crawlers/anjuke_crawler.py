import xlwt
from lxml import etree
import requests
import time,random

all_info_list = []

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


def get_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    infos = selector.xpath('//*[@class="zu-itemmod"]')
    for info in infos:
        title = info.xpath('div[1]/h3/a/b/text()')[0].strip()
        yangshi = info.xpath('div[1]/p[1]/b[1]/text()')[0]+info.xpath('div[1]/p[1]/b[2]/text()')[0]
        mianji = info.xpath('div[2]/div[2]/span[2]/text()')[0]
        niandai = info.xpath('div[2]/div[2]/span[4]/text()')
        dizhi = info.xpath('div[2]/div[3]/span/text()')[0].strip()
        danjia = info.xpath('div[3]/span[2]/text()')
        zongjia1 = info.xpath('div[3]/span[1]/strong/text()')
        zongjia2 = info.xpath('div[3]/span[1]/text()')
        zongjia = zongjia1 + zongjia2
        biaoqians = info.xpath('//span')
        t = []
        for biaoqian in biaoqians:
            t.append(biaoqian.xpath('text()'))
        info_list = [title, yangshi, mianji, niandai, dizhi, danjia, zongjia]
        all_info_list.append(info_list)

    time.sleep(1)


if __name__ == '__main__':
    urls = ['https://sh.zu.anjuke.com/p{}'.format(str(i)) for i in range(1, 51)]
    for url in urls:
        get_info(url)

    header = ['序号', '标题', '样式', '面积', '年代', '地址', '单价（元/平方）', '总价（万元）']
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

    book.save('hangzhouershoufang.xls')