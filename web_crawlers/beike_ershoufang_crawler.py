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
    house_list = soup.find_all('li', class_='clear xiaoquListItem CLICKDATA')
    for house in house_list:
        try:
            title = house.find_all('a', class_='maidian-detail')[1].string
            print(title)
            all_info = house.find_all('div',class_='positionInfo')[0]
            infos = all_info.get_text().strip()
            jiancheng = infos.find("年建成")
            year = infos[jiancheng-4:jiancheng]

            danjias = house.find_all("div",class_="totalPrice")[0]
            danjia = danjias.find_all("span")[0].string


            
            info_list = [title, year, danjia]
            all_info_list.append(info_list)
        except:
            continue
    
    time.sleep(1)


if __name__ == '__main__':
    header = ['小区', '年代', '二手房均价']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    
    urls = ['https://sh.ke.com/xiaoqu/pg{}/'.format(str(i)) for i in range(1,101)]
    i = 1  # 行
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
            j = 0  # 列
            for data in list:  # 列数据
                sheet.write(i, j, data)
                j += 1
            i += 1

    book.save('beiker-xiaoqu.xls')
    print(i)
