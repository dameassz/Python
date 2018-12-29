
# coding: utf-8

# In[1]:


import random
import time

import requests
from openpyxl import Workbook
import pymssql


# In[2]:


def get_conn():
    '''建立数据库连接'''
    conn = pymssql.connect(server='localhost', user='sa', password='Xinge', database='Python')
    return conn


# In[3]:


def insert(conn, info):
    '''数据写入数据库'''
    with conn.Cursor as cursor:
        sql = "INSERT INTO `python` (`shortname`, `fullname`, `industryfield`, `companySize`, `salary`, `city`, `education`) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, info)
    conn.commit()


# In[7]:


def get_json(url, page, lang_name):
    '''返回当前页面的信息列表'''
    '''eaders = {
        'Host': 'www.lagou.com',
        'Connection': 'keep-alive',
        'Content-Length': '23',
        'Origin': 'https://www.lagou.com',
        'X-Anit-Forge-Code': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'X-Anit-Forge-Token': 'None',
        'Referer': 'https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
    }'''
    
    headers = {'Accept':'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'56',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    #Cookie:LGUID=20161214153335-9f0eacc2-c1cf-11e6-bd6c-5254005c3644; user_trace_token=20180122030442-efefe00e-fedd-11e7-b2cb-525400f775ce; LG_LOGIN_USER_ID=e619b07cb5d026e017473de3d4ef1bb5a3da9a0ddd6ea0a5; gray=resume; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%227288096%22%2C%22%24device_id%22%3A%221626117eb3016-0703ff024b7ae5-71292b6e-1049088-1626117eb3569%22%2C%22first_id%22%3A%221626117eb3016-0703ff024b7ae5-71292b6e-1049088-1626117eb3569%22%7D; WEBTJ-ID=20180403125347-16289da9860300-0dcabf1bb6b166-71292b6e-1049088-16289da98619b; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73739; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; gate_login_token=63a7401b950e42d41a03d8ce1db134ac22aeefc46c120c43; index_location_city=%E6%B7%B1%E5%9C%B3; JSESSIONID=ABAAABAAADEAAFIDFE252684FD90098F44851E32F917A9F; TG-TRACK-CODE=search_code; SEARCH_ID=e267bafce9b0431d8f8a867e48f2a7bf; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522167431,1522215930,1522219100,1522731245; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1522741185; _gat=1; _ga=GA1.2.983742987.1481700649; _gid=GA1.2.1178844706.1522731227; LGSID=20180403154252-9d580c63-3712-11e8-b228-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%25E6%2595%25B0%25E6%258D%25AE%25E5%2588%2586%25E6%259E%2590%3Fcity%3D%25E6%25B7%25B1%25E5%259C%25B3%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGRID=20180403154252-9d580e4e-3712-11e8-b228-525400f775ce; _putrc=2C1A435C1A81EDB8
    'Host':'www.lagou.com',
    'Origin':'https://www.lagou.com',
    'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90?city=%E6%B7%B1%E5%9C%B3&cl=false&fromSearch=true&labelWords=&suginput=',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36',
    'X-Anit-Forge-Code':'0',
    'X-Anit-Forge-Token':'None',
    'X-Requested-With':'XMLHttpRequest'}
    
    data = {'first': 'false', 'pn': page, 'kd': lang_name}
    json = requests.post(url, data, headers=headers).json()
    list_con = json['content']['positionResult']['result']
    info_list = []
    for i in list_con:
        info = []
        info.append(i.get('companyShortName', '无'))  # 公司名
        info.append(i.get('companyFullName', '无'))
        info.append(i.get('industryField', '无'))   # 行业领域
        info.append(i.get('companySize', '无'))  # 公司规模
        info.append(i.get('salary', '无'))   # 薪资
        info.append(i.get('city', '无'))
        info.append(i.get('education', '无'))   # 学历
        info_list.append(info)
    return info_list   # 返回列表


# In[8]:


def main():
    lang_name = 'python'
    wb = Workbook()  # 打开 excel 工作簿
    #conn = get_conn()  # 建立数据库连接  不存数据库 注释此行
    for i in [ '上海', '深圳','重庆','成都']:   # 五  个城市
        page = 1
        ws1 = wb.active
        ws1.title = lang_name
        url = 'https://www.lagou.com/jobs/positionAjax.json?city={}&needAddtionalResult=false'.format(i)
        while page < 31:   # 每个城市30页信息
            info = get_json(url, page, lang_name)
            page += 1
            time.sleep(random.randint(10, 20))
            #for row in info:
                #insert(conn, tuple(row))  # 插入数据库，若不想存入 注释此行
                #ws1.append(row)
    #conn.close()  # 关闭数据库连接，不存数据库 注释此行
    wb.save('{}职位信息.xlsx'.format(lang_name))

if __name__ == '__main__':
    main()


# In[3]:


help(pymssql)


# In[ ]:


pymssql.Cursor

