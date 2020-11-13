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
def get_image_number(soup):
    positions = {"0":None,"21.4":None,"42.8":None,"64.2":None,"85.6":None,"107":None,"128.4":None,"149.8":None,"171.2":None,"192.6":None}
    pos_keys = ["0","21.4","42.8","64.2","85.6","107","128.4","149.8","171.2","192.6"]
    
    price=str(soup.findAll('span', 'num')[1])
    print(price)
    startStr='background-image:'
    endStr='.png'
    photo = re.search('%s.*%s' % (startStr, endStr),price)
    photo = photo.group()[22:]
    image = requests.get('http:' + photo).content
    f = open('price.png', 'wb')
    f.write(image)
    f.close()
    num = []
    number = pytesseract.image_to_string(Image.open("price.png"),config="--psm 8 -c tessedit_char_whitelist=1234567890")
    print(number)
    
    for i in range(10):
        positions[pos_keys[i]] = number[i]
    return positions

def get_info(soup,positions,all_info_list):
    house_list = soup.find_all('div', class_='item')
    for house in house_list:
        try:
            title = house.find_all('h5')[0].string
                
            shi = title.find("室")
            shi = title[shi-1]
            ting = title.find("厅")
            ting = title[ting-1]
                
            mianjilouceng_dizhi = house.find_all('div',class_="desc")[0]
            mianjilouceng = mianjilouceng_dizhi.find_all('div')[0].string
            seperate = mianjilouceng.find("|")
            mianji = mianjilouceng[:seperate-2]
            louceng = mianjilouceng[seperate+2:-1]

            dizhi = mianjilouceng_dizhi.find_all('div')[1].string.strip()

            danjias = house.find_all("span",class_="num")
            unit = house.find_all("span",class_="unit")[0]
            danjia = ""
            for digit in danjias[:]:
                link = digit["style"]
                minus = link.rfind("-")
                position = link[minus+1:-2]
                danjia += positions[position]
            if unit.string == "/天":
                danjia = str(int(danjia)*30)
            
            bq = house.find_all('div',class_="tag")[0]
            biaoqians = bq.find_all('span')
            
            t = ''
            for biaoqian in biaoqians:
                t+=(biaoqian.string)

            
            info_list = [title, shi, ting, mianji, louceng, dizhi, danjia, t]
            all_info_list.append(info_list)
        except:
            continue
    
    time.sleep(1)


if __name__ == '__main__':
    header = ['标题', '室', '厅', '面积', '楼层', '地址', '价格', '标签']
    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('Sheet1')
    for h in range(len(header)):
        sheet.write(0, h, header[h])
    
    urls = ['http://sh.ziroom.com/z/z2-p{}/'.format(str(i)) for i in range(1,51)]
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
        num = get_image_number(soup)
        get_info(soup,num,all_info_list)

    
    
        for list in all_info_list:  # 行数据
            j = 0  # 列
            k += 1
            for data in list:  # 列数据
                sheet.write(i, j, data)
                j += 1
            i += 1

    book.save('../datasets/ziroom.xls')
    print(i,k)
