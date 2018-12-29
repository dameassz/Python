
# coding: utf-8

# In[1]:


# -*- coding: utf-8 -*-
import json
import pymssql
from collections import OrderedDict


# In[2]:


def get_data():
    with open('D:\Xinge_Techonology\Temp_Working_Zone\住宅建筑.json', 'r') as f:
        SHP = json.load(f)  # 解析每一行数据
    return SHP


# In[3]:


def get_target_value(key, dic, tmp_list):
    """
    :param key: 目标key值
    :param dic: JSON数据
    :param tmp_list: 用于存储获取的数据
    :return: list
    """
    if not isinstance(dic, dict) or not isinstance(tmp_list, list):  # 对传入数据进行格式校验
        return 'argv[1] not an dict or argv[-1] not an list '

    if key in dic.keys():
        tmp_list.append(dic[key])  # 传入数据存在则存入tmp_list
    else:
        for value in dic.values():  # 传入数据不符合则对其value值进行遍历
            if isinstance(value, dict):
                get_target_value(key, value, tmp_list)  # 传入数据的value值是字典，则直接调用自身
            elif isinstance(value, (list, tuple)):
                _get_value(key, value, tmp_list)  # 传入数据的value值是列表或者元组，则调用_get_value
    return tmp_list


def _get_value(key, val, tmp_list):
    for val_ in val:
        if isinstance(val_, dict):  
            get_target_value(key, val_, tmp_list)  # 传入数据的value值是字典，则调用get_target_value
        elif isinstance(val_, (list, tuple)):
            _get_value(key, val_, tmp_list)   # 传入数据的value值是列表或者元组，则调用自身


# In[257]:


def replace(values, T_list):
    if  not isinstance(T_list,list):
        return 'T_list is not list'
    for k in values:
        if isinstance(k,list) and len(k) != 2:
            replace(k,T_list)
        else:
            k = str(k).replace(",","")
            #values = str_poi
            #print(k)
    return values


# In[258]:


v = replace(Position, [])


# In[259]:


v


# In[4]:


if __name__ == '__main__':
    a=get_data()
    Floor = get_target_value("妤煎眰",a,[])
    Position = get_target_value("paths",a,[])
    FID = get_target_value("FID",a,[])
    #data_insert(B)


# In[5]:


Floor.remove('妤煎眰')
FID.remove('FID')


# In[7]:


Floor


# In[8]:


FID


# In[9]:


str_poi = OrderedDict()
for i in range(len(Position)):
    str_poi[i] = str(Position[i][0]).replace("[","(")
    str_poi[i] = str_poi[i].replace("]",")")
    str_poi[i] = str_poi[i].replace(",","")


# In[10]:


list(str_poi)


# In[12]:


Buildings = [{
    "FID" : FID[i],
    "Floor" : Floor[i],
    "Geometry" : "POLYGON Z" + str_poi[i]
}
for i in str_poi.keys() and range(len(Floor)) and range(len(FID))
]


# In[13]:


Buildings


# In[14]:


from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.exc import IntegrityError, DatabaseError


# In[15]:


metadata = MetaData()
engine = create_engine('mssql+pymssql://sa:Xinge2018@192.168.17.8:1433/FieldArrange')
Build = Table('Buildings', metadata,
                extend_existing=True,
                autoload=True,
                autoload_with=engine)


# In[16]:


def InsertData(engine, table, values):
    conn = engine.connect()
    transaction = conn.begin()
    try:
        ins = table.insert()
        conn.execute(ins,values)
        transaction.commit()
    except DatabaseError as error:
        transaction.rollback()
        print(error)
    finally:
        conn.close()


# In[18]:


InsertData(engine, Build, Buildings)

