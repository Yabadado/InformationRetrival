from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
from urllib.error import HTTPError
import urllib
import re
import sqlite3
from selenium import webdriver
import json
import requests
import time
import tkinter as tk


result_item = []
result_price = []
result_link = []

def productsearch(main):
    global momosearch       #momo購物網
    global pchomesearch     #pchome購物
    global yahoosearch      #奇摩商城
    global shpsearch        #蝦皮
    global itemname         #商品名稱

    global result_item       # 結果的商品名稱
    global result_price      # 結果的商品價錢
    global result_link      # 結果的商品連結

    str(main)
    momo = 'https://www.momoshop.com.tw/search/searchShop.jsp?keyword='
    momosearch=momo=main
    pchome = 'http://ecshweb.pchome.com.tw/search/v3.3/all/results?q='
    pchomesearch = pchome+main

    yahoo = 'https://tw.search.mall.yahoo.com/search/mall/product?p='
    yahoosearch = yahoo+main

    shp_f='https://shopee.tw/search/?keyword='
    shp_e='&sortBy=sales'
    shpsearch=shp_f+main+shp_e


    #print("MOMO購物網:")
    #print(momosearch)
    #momoinfo
    print("PcHome24H購物:")
    print(pchomesearch)
    pchomeinfo()
    print("YAHOO超級商城:")
    print(yahoosearch)
    yahooinfo()
    print("蝦皮購物:")
    print(shpsearch)
    shpinfo()
    '''
    for index in range(len(result_item)):
        print(result_item[index])
        print(result_price[index])
        print(result_link[index])
        print()
    '''
    #res_print()

def pchomeinfo():
    global pchomseaarch

    res = requests.get(pchomesearch)
    ress = res.text

    jd = json.loads(ress)

    global result_item  # 結果的商品名稱
    global result_price  # 結果的商品價錢
    global result_link  # 結果的商品連結

    pcitems=[]
    pcprices=[]
    pcurls=[]
    pcmainurl='http://24h.pchome.com.tw/prod/'
    try:

        for item in jd['prods']:
            pcitems.append(item['name'])
            pcprices.append(item['price'])
            url=pcmainurl+item['Id']
            pcurls.append(url)

        pcitems0=pcitems[0]
        pcprices0=pcprices[0]
        pcurls0=pcurls[0]


    except:
        pcitems0="查無此項"
        pcprices0="t查無此項"
        pcurls0="查無此項"
    #pcmatch(pcitems0)

    for index in range(len(pcitems)):
        #print(pcitems[index])
        result_item.append(pcitems[index])
        #print(pcprices[index])
        result_price.append(pcprices[index])
        #print(pcurls[index])
        result_link.append(pcurls[index])
        #print(pcimgs[index])
        #print()

def yahooinfo():
    global yahoosearch
#--------------透過瀏覽器爬蟲--------------------------
    chromedriver = "C:\selenium_driver\chromedriver.exe"    #打開chromedriver
    driver = webdriver.Chrome(chromedriver)                 #
    driver.get(yahoosearch)                                 #把網址傳給driver
    ps = driver.page_source                                 #抓下網頁原始碼

#-----------全域 結果-----------
    global result_item
    global result_price
    global result_link

    yaitn = []
    yaitp = []
    yaitul = []
    #print(ps)
    sp = BeautifulSoup(ps, "lxml")
    try:
        itemname = sp.findAll("span", {"class":"BaseGridItem__title___2HWui"})
        itemprice = sp.findAll("em", {"class":"BaseGridItem__price___31jkj"})
        itemurl=sp.select('a[href^="https://tw.mall.yahoo.com/item/"]')
        for itpp in itemprice:
            yaitp.append(itpp.text)
            #print(itpp.text)
        for itnn in itemname:
            yaitn.append(itnn.text)
            #print(itnn.text)
        for itull in itemurl:
            yaitul.append(itull.get('href'))
            #print(itull.get('href'))

        yaitn0 = yaitn[0]
        yaitp0 = yaitp[0]
        yaitul0 = yaitul[0]

    except:
        yaitn0="查無此項"
        yaitp0="查無此項"
        yaitul0="查無此項"
    #yamatch(yaitn0)

    for index in range(len(yaitp)):
        #print(yaitn[index])
        result_item.append(yaitn[index])
        #print(yaitp[index])
        result_price.append(yaitp[index])
        #print(yaitul[index])
        result_link.append(yaitul[index])
        #print(pcimgs[index])
        #print()
    driver.close()

def shpinfo():
    global shpsearch
    chromedriver = "C:\selenium_driver\chromedriver.exe"
    driver = webdriver.Chrome(chromedriver)

    driver.get(shpsearch)
    time.sleep(5)
    ps = driver.page_source

    driver.close()
    #print(ps)
    sp = BeautifulSoup(ps, "lxml")
    spitemss = sp.findAll("div", {"class": "_1NoI8_ KQFWxC"})
    sppricess = sp.findAll("div", {"class": "tyA3vN _3eZ5Vz _3RuPcU"})
    spurlss = sp.findAll("div",{"class":"col-xs-2-4 shopee-search-item-result__item"})
    #print(spurlss)

    # -----------全域 結果-----------
    global result_item
    global result_price
    global result_link

    spitems = []
    spprices = []
    spurls = []
    sprull = 'https://shopee.tw'

    for spitem in spitemss:
        spitems.append(spitem.text)
    for spprice in sppricess:
        spprices.append(spprice.text)
    for spurl in spurlss:
        for a in spurl.findAll('a',href=True):
            url=a['href']
            url = urllib.parse.quote(url)
            spurls.append(sprull+url)
            #print(url)
    for index in range(len(spitems)):
        #print(spitems[index])
        result_item.append(spitems[index])
        #print(spprices[index])
        result_price.append(spprices[index])
        #print(spurls[index])
        result_link.append(spurls[index])
        #print()

'''
#-----------產生視窗參數------------
window = tk.Tk()
window.title('my window')
window.geometry('800x600')
window.resizable(0,0)

#-----------變數-----------------
var = tk.StringVar()    # 这时文字变量储存器
l = tk.Label(window,
    textvariable=var,   # 使用 textvariable 替换 text, 因为这个可以变化
    bg='green', font=('Arial', 12), width=15, height=2)
l.pack()

#-----定義事件-------
def hit_me():
    global on_hit
    if on_hit == False:     # 从 False 状态变成 True 状态
        on_hit = True
        var.set('you hit me')   # 设置标签的文字为 'you hit me'
    else:       # 从 True 状态变成 False 状态
        on_hit = False
        var.set('') # 设置 文字为空

#--------按鈕------------
btn = tk.Button(window,
    text='hit me',      # 显示在按钮上的文字
    width=15, height=2,
    command=hit_me)     # 点击按钮式执行的命令
btn.pack()    # 按钮位置
on_hit = False  # 默认初始状态为 False


#---------視窗產生------
window.mainloop()

'''

def res_print():
    for index in range(len(result_item)):
        print(index+1,':')
        print(result_item[index])
        print(result_price[index])
        print(result_link[index])
        print()