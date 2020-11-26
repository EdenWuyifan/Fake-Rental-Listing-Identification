import xlwt
from lxml import etree
import requests
import time
import random
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


# getting randomized number image using tenseract

def get_info(soup, all_info_list):
    house_list = soup.find_all('div', class_='li-itemmod')
    for house in house_list:
        try:
            title = house.find_all('div', class_='li-info')[0]
            title = title.find_all("a")[0].string

            shi = house.find_all('p', class_="date")[0].string
            ting = house.find_all('div', class_="li-side")[0]
            ting = ting.find_all("strong")[0].string

            info_list = [title, shi, ting]
            all_info_list.append(info_list)
        except:
            continue

    time.sleep(1)


if __name__ == '__main__':
    header = ['', '小区', '竣工日期', '二手房均价']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])

    urls = [
        'https://shanghai.anjuke.com/community/p{}'.format(str(i)) for i in range(1, 51)]
    i = 1  # 行
    k = 1  # 序号
    for url in urls:
        all_info_list = []
        browser = webdriver.Chrome(ChromeDriverManager().install())
        wait = WebDriverWait(browser, 10)
        browser.get(url)
        html_data2 = browser.page_source.encode('utf-8')
        browser.close()
        soup = bs(html_data2, 'html.parser')
        get_info(soup, all_info_list)

        for list in all_info_list:  # 行数据
            j = 1  # 列
            sheet.write(i, 0, k)
            k += 1
            for data in list:  # 列数据
                sheet.write(i, j, data)
                j += 1
            i += 1

    book.save('anjuke_xiaoqu.xls')
    print(i, k)
