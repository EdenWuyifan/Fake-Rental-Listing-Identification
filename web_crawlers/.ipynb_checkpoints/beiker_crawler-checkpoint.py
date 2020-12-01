import xlwt
from lxml import etree
import requests
import time,random
import re
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}


#getting randomized number image using tenseract

def get_info(soup,all_info_list):
    house_list = soup.find_all('div', class_='content__list--item')
    for house in house_list:
        try:
            title = house.find_all('a', class_='twoline')[0].string
            #print(title)
            all_info = house.find_all('p',class_='content__list--item--des')[0]
            infos = all_info.get_text().strip()
            shi = infos.find("室")
            shi = infos[shi-1]
            ting = infos.find("厅")
            ting = infos[ting-1]

            mianji = infos.find("㎡")
            mianji = infos[mianji-5:mianji].strip()

            lou = infos.find("（")
            ceng = infos.find("）")
            louceng = infos[lou+1:ceng-1]
            #print(louceng)
            
            dizhis = all_info.find_all('a')
            dizhi = dizhis[0].string+dizhis[1].string+dizhis[2].string
            #print(dizhi)

            danjias = house.find_all("span",class_="content__list--item-price")[0]
            
            unit = danjias.get_text().strip()
            danjia = danjias.find_all("em")[0].string
            if unit[-1] == "天":
                danjia = str(int(danjia)*30)

            
            bq = house.find_all('p',class_="content__list--item--bottom oneline")[0]
            biaoqians = bq.find_all('i')
            
            t = ''
            for biaoqian in biaoqians:
                t+=(biaoqian.string)

            
            info_list = [title, shi, ting, mianji, louceng, dizhi, danjia, t]
            all_info_list.append(info_list)
        except:
            continue
    
    time.sleep(1)


if __name__ == '__main__':
    header = ['序号', '标题', '室', '厅', '平米', '楼层', '地址', '价格', '标签']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    
    urls = ['https://sh.zu.ke.com/zufang/pg{}rt200600000001/#contentList'.format(str(i)) for i in range(301,601)]
    i = 1  # 行
    k = 1  # 序号
    for url in urls:
        all_info_list = []
        browser=webdriver.Chrome(ChromeDriverManager().install())
        wait=WebDriverWait(browser, 10)
        browser.get(url)
        html_data2 = browser.page_source.encode('utf-8')
        browser.close()
        soup = bs(html_data2, 'html.parser')
        get_info(soup,all_info_list)

    
    
        for list in all_info_list:  # 行数据
            j = 1  # 列
            sheet.write(i, 0, k)
            k += 1
            for data in list:  # 列数据
                sheet.write(i, j, data)
                j += 1
            i += 1

    book.save('beiker-new.xls')
    print(i,k)
