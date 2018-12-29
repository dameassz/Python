
# coding: utf-8

# In[1]:


import pandas_datareader as web
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import mpl_finance as mpf


import matplotlib.dates as dates


# In[2]:


Goo = web.get_data_yahoo('Goog','2017-1-1','2018-1-1') #time, open, close, high, low, ...


# In[3]:


Goo


# In[4]:


G = pd.DataFrame(Goo,columns = ['Open','Close','High','Low'])


# In[5]:


G


# In[8]:


from matplotlib.pylab import date2num
import datetime


# In[18]:


Goog_mat=G.as_matrix()


# In[9]:


def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d') 
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time
# dataframe转换为二维数组

mat_G = G.values
num_time = date_to_num(mat_G[:,0])
mat_G[:,0] = num_time


# In[20]:


ax = plt.subplots(figsize  = (8,5))


# In[26]:


p = mpf.candlestick_ochl(ax,G,0.6,'b','r')


# In[16]:


help(mpf.candlestick_ochl)


# In[11]:


import matplotlib as mpl
import tushare as ts
import matplotlib.pyplot as plt
import mpl_finance as mpf
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['fangsong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

wdyx = ts.get_k_data('600516','2017-1-1','2018-1-1')#选取股票
wdyx.info()
wdyx[:3]
from matplotlib.pylab import date2num
import datetime
def date_to_num(dates):
    num_time = []
    for date in dates:
        date_time = datetime.datetime.strptime(date,'%Y-%m-%d') 
        num_date = date2num(date_time)
        num_time.append(num_date)
    return num_time
# dataframe转换为二维数组

mat_wdyx = wdyx.values
num_time = date_to_num(mat_wdyx[:,0])
mat_wdyx[:,0] = num_time


'''
# 日期, 开盘, 收盘, 最高, 最低, 成交量, 代码



fig, ax = plt.subplots(figsize=(15,5))
fig.subplots_adjust(bottom=0.5)
mpf.candlestick_ochl(ax, mat_wdyx, width=0.6, colorup='g', colordown='r', alpha=1.0)
plt.grid(True)
# 设置日期刻度旋转的角度 
plt.xticks(rotation=30)
plt.title('drink wine?')
plt.xlabel('Date')
plt.ylabel('Price')
# x轴的刻度为日期
ax.xaxis_date ()

'''
fig, (ax1, ax2) = plt.subplots(2, sharex=True, figsize=(15,8))

mpf.candlestick_ochl(ax1, mat_wdyx, width=0.6, colorup = 'r', colordown = 'g')
ax1.set_title('上证指数 ')
ax1.set_ylabel('价格')
ax1.grid(True)
ax1.xaxis_date()
plt.bar(mat_wdyx[:,0], mat_wdyx[:,5], width= 0.6)
ax2.set_ylabel('成交量')
ax2.grid(True)

plt.show()


# In[39]:


wdyx

