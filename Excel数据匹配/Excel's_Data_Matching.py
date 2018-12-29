
# coding: utf-8



import pandas as pd
import os,sys




DF = pd.read_excel(r'D:\Xinge_Techonology\Temp_Working_Zone\重庆江北摄像头导入模板&设备信息\摄像头匹配坐标标准表.xls')







os.chdir(r'D:\Xinge_Techonology\Temp_Working_Zone\重庆江北摄像头导入模板&设备信息\重庆江北摄像头设备信息')




arr = ['寸滩派出所','大石坝派出所','大兴村派出所','复盛派出所','港城园派出所','观音桥派出所',
      '郭家沱派出所','红旗河沟派出所','花园村派出所','华新街派出所','江北城派出所','石马河派出所',
      '石门派出所','唐家沱派出所','五宝派出所','五里店派出所','鱼嘴派出所']




for i in arr:
    df = pd.read_excel(i+'.xls')
    for x in DF.index:
        for y in df.index:
            if DF.监控点名称[x] == df['监控点名称'][y]:
                DF['设备编码'][x] = df['设备编码'][y]
                DF['备注'][x] = df['备注'][y]




DF




DF.to_excel(r'D:\Xinge_Techonology\Temp_Working_Zone\重庆江北摄像头导入模板&设备信息\设备信息表.xls')

