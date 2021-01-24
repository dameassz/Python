import re 
import requests
import pandas as pd
import xlsxwriter
from bs4 import BeautifulSoup 
import selenium
from selenium import webdriver

def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_Html(url):
    # ....
    retry_count = 5
    proxy = get_proxy().get("proxy")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    #.chrome_options.add_argument('--proxy-server=http://{}'.format(get_proxy().get("proxy")))
    driver = webdriver.Chrome(options = chrome_options)
    while retry_count > 0:
        try:
            driver.get(url, proxies={"http": "http://{}".format(proxy)},headers = headers)
            html = driver.page_source
            return html
        except Exception:
            retry_count -= 1
    # 删除代理池中代理
    delete_proxy(proxy)
    return None

    
def Get_Info(Html):
    H_soup = BeautifulSoup(Html.contents,'html.parser')

    for soup in H_soup.find_all('div',class_ = 'job-primary'):
        Job_Name = soup.find('span',class_ = 'job-name').text
        Salary = soup.find('div',class_ = 'job-limit clearfix').find(class_ = 'red').text
        Experience = soup.find('div',class_ = 'job-limit clearfix').find('p').contents[0]
        Education = soup.find('div',class_ = 'job-limit clearfix').find('p').contents[2]
        Job_Tag = [span.text.replace('\n',' ') for span in soup.find_all(class_ = 'tags')]
        Company = soup.find('div',class_ = 'company-text').find('a').text
        Industry = soup.find('a',class_ = 'false-link').text
        Address = soup.find(class_ = 'job-area').text
        X_Round_Fin = soup.find('div',class_ = 'info-company').find('p').contents[2]
        Staff_Size = soup.find('div',class_ = 'info-company').find(string = re.compile("人"))
        Benefit = soup.find('div',class_ = 'info-desc').text
    
        D_url= 'https:/www.zhipin.com{}?ka=search_list_jname_32_blank&lid=2ZyaKdskciw.search.32&srcReferer={}'.format(soup.find('span',class_ = 'job-name').a.get('href'),url )
            
        List = [Job_Name,Salary,Experience,Education,Job_Tag,Company,Industry,Address,X_Round_Fin,Staff_Size,Benefit,D_url]
        return List
            
        #List = []
        #time.sleep(random(0,3))'''

def main():
    '''headers = {
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
'cookie': '_bl_uid=7pkpbiUp5g0y9Xx01hb721ztUFg7; lastCity=100010000; __zp_seo_uuid__=9cd1a1c8-9d9f-40e1-8486-e23b2aa1214f; toUrl=https%3A%2F%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fresume%3Fka%3Dheader-resume; JSESSIONID=""; __g=-; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DsQMz70zf-C5AEe0gc3h07v4-l3-Ll0NDZfwZIVHZS0R9lO731pFul9FWd5CtwFL4%26wd%3D%26eqid%3Debf9975c0002256f000000065fd85c9e&l=%2Fwww.zhipin.com%2F&s=3&friend_source=0&g=&s=3&friend_source=0; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1607757911,1608015010,1608015017,1609852833; ___gtid=-1184928907; __fid=97c2dc0f0c35f2a9024b270fca85d8d4; __c=1607523235; __a=86076755.1606543728.1606964653.1607523235.197.4.18.8; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1609852862; __zp_stoken__=4adfbYWhHSmUhORRLGQ0ZDmNJNDptV3EuBQRkLSsEUR5LKE10P0k2UA58bmotJxo6Nn81DH9EKEJ9dUwCVQJ7EEggeVtGJHhwaAghagIaMjNtPj9BTXYLPV58dz0GA2RSMC4%2FHzs%2FLUQNDVphRg%3D%3D; __zp_sseed__=TrXJj9JWp1K9UXSXDYE+6CY8Nu7774j26+yd8QYIPLs=; __zp_sname__=cf18b6df; __zp_sts__=1609852894050'
}
    session = requests.session()''' 
    DF = pd.DataFrame(columns = ['Job_Name','Salary','Experence','Education','Job_Tag','Company','Industry','Address','X_Round_Fin','Staff_Size','Benefits','Url'])
    SH_DF = DF
    SZ_DF = DF
    CQ_DF = DF
    CD_DF = DF    
    for city in ['101020100','101280600','101040100','101270100']:                   
        #101020100-->上海   101280600-->深圳   101040100-->重庆  101270100-->成都
        url = ['https://www.zhipin.com/c{0}/?query=金融数据分析&page={1}&ka=page-{1}'.format(city,i)for i in range(1,11)]
        for i in url:
            html = get_Html(i)
            #List = Get_Info(html)
            print(html)
            '''List = pd.DataFrame(List).T
            List.columns = DF.columns
            
            if city == '101020100':
                SH_DF = SH_DF.append(List)
            elif city == '101280600':
                SZ_DF = SH_DF.append(List)
            elif city == '101040100':
                CQ_DF = SH_DF.append(List)
            else :
                CD_DF = SH_DF.append(List)'''
                
if __name__ = __main():
    main()