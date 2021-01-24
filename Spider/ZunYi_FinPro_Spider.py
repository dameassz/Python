# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 20:08:36 2020

@author: ZZH
"""

import re
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter

option = webdriver.ChromeOptions()
option.add_argument('--headless')  # 开启无界面模式
option.add_argument('--disable-gpu')  # 禁用gpu，解决一些莫名的问题
driver = webdriver.Chrome(options=option)
driver.maximize_window()

B_DF = pd.DataFrame(columns=['产品名','公司名','参考利率范围','融资额度','融资期限','担保方式','申请条件','产品简介','适用客户','提交材料','产品特点'])
E_DF = pd.DataFrame(columns=['产品名','公司名','参考担保费利率范围','融资担保额度','融资担保期限','产品类型','申请条件','产品简介','适用客户','提交材料','产品特点'])
for keyword in range(1,248):
    driver.get("http://zunyi.smefintech.com/product/detail?productId="+str(keyword))
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    h = soup.find("div",class_="mainwraper")
    
    Detail_Proname = h.find("h3",id="detail_proname")
    Product_Name = str(Detail_Proname.get_text(strip = True)).replace('企业个人','')                 #获取产品名

    Com_Name = h.find("span",id="detail_finname").get_text(strip =True)  #获取机构名

    List = [Product_Name,Com_Name]
    
    for i in h.find_all("ul",limit = 4):
        T_List = [text for text in i.stripped_strings][1]
        List.append(T_List)
    for i in h.find_all("tr"):
        T_List = [text for text in i.stripped_strings][1]
        List.append(T_List)                                              #获取产品详细细节
    if '银行' in h.find("span",id="detail_finname").string: 
        List = pd.DataFrame(List).T 
        List.columns = B_DF.columns
        B_DF = B_DF.append(List)
    else:
        List = pd.DataFrame(List).T 
        List.columns = E_DF.columns
        E_DF = E_DF.append(List)
    List = []
    
driver.close()
writer = pd.ExcelWriter(r'C:\Users\ZZH\Desktop\Fin_Pro_Info.xls',engine='xlsxwriter')
workbook = writer.book
B_DF.to_excel(writer,'债权融资',index=False)
E_DF.to_excel(writer,'融资担保',index=False)
workbook.close
writer.save()