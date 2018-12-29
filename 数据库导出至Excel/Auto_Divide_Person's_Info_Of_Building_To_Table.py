
# coding: utf-8



from sqlalchemy import create_engine
from collections import OrderedDict

import pymssql
import os, sys
import pandas as pd
import xlsxwriter




def MakeDirs(dic,maindir):
    for y in dic.values():
        os.mkdir(os.path.join(maindir,y))




def ReadType(conn):
    Type_sql = "Select TypeFlagName,TypeName,TypeNum from T_Type where TypeFlagName not like '企业%'"
    Type_df = pd.read_sql_query(Type_sql,conn)
    return Type_df




def ReadHouseInfo(Address,conn):
    R_sql =  """Select B.Address,F.Name,H.HouseName,H.Code,H.IsCun,H.IsDormitory from T_Building B 
                left join T_Floor F on B.Code = F.ParentCode 
                left join T_House H on F.Code = H.ParentCode where B.Address = """
    Room_sql = R_sql + "'" + Address + "'"
    Room_df = pd.read_sql_query(Room_sql,conn)
    return Room_df




def ReadPersonInfo(Address,Area,conn):
    P_sql =  """Select [Name], [IdCard], [Sex], [HouseCode], [Age], [NativePlace], [Nation], [PoliticalStatus], [Education], [WorkUnit], 
                [PhoneNum], [Address], [LivingAddress], [CarNum], [Housemaster], [IsPermanentPopulation], [IsKeyPopulation], 
                [ImportantPeopleCategory], [IsSelfRoom], [BuyDate], [Remark], [MarriageStatus] from T_People Where LivingAddress like"""
    
    S_sql =  """Select [Name], [Sex], [IdCard], [Age], [PoliticalStatus], [StudentId], [University], [Academy], [Major], [Grade], 
                [Class], [Dormitory], [RoomCode], [NativePlace], [FamilyPlace] from T_Student Where Dormitory like"""
    
    if Area == "贵安数字经济产业园" or Area == "摆井安置小区" or Area == "翁岩安置小区" or Area == "大坝井安置房":
        People_sql = P_sql + "'" + Address + "%" + "'" 
        People_df = pd.read_sql_query(People_sql,conn)
        return People_df
    else:
        Student_sql = S_sql + "'" + Address + "%" + "'"
        Student_df = pd.read_sql_query(Student_sql,conn)
        return Student_df




def StandardFormat(workbook,worksheet,Headings_list,df):
    Row_Format = workbook.add_format({'fg_color' : '#D2E9FF'})
    #Col_Format = workbook.add_format({'num_format': 49})
    CHeader_Format = workbook.add_format({
        'bold' : True ,
        'text_wrap' : True ,
        'font_name' : '黑体',
        'font_size' : 12 ,
        'align' : 'center' ,
        'fg_color' : '#D2E9FF' ,#D2E9FF
        'border': 1})
    EHeader_Format = workbook.add_format({
        'bold' : True ,
        'text_wrap' : True ,
        'font_name' : 'Times New Roman',
        'font_size' : 12 ,
        'align' : 'center' ,
        'fg_color' : '#D2E9FF' ,#D2E9FF
        'border': 1})
    
    worksheet.write_row('A1',Headings_list,CHeader_Format)   
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(1,col_num,value,EHeader_Format)
        
    worksheet.set_row(0,30)
    worksheet.set_row(1,30) 
    for i in df.index:
        worksheet.set_row(i+2,18)
    """if worksheet.name == "RoomRef":
        worksheet.set_column('D:D',Col_Format)
    elif worksheet.name == "PeopleInfo":
        worksheet.set_column('B:B',Col_Format)
        worksheet.set_column('D:D',Col_Format)
        worksheet.set_column('K:K',Col_Format)
    elif worksheet.name == "StudentInfo":
        worksheet.set_column('C:C',Col_Format)
        worksheet.set_column('F:F',Col_Format)
        worksheet.set_column('M:M',Col_Format)"""




def MakeExcel(dic,maindir,con):
    AreaFile = os.listdir(maindir)
    conn = con
    
    T_Headings = ["类型标识名","类型名","类型编码"]
    R_Headings = ["楼栋地址","楼层","房间号","房屋号","是否农村住宅","是否学生宿舍"]
    P_Headings = ["姓名","身份证","性别","房子盒子编码","年龄","籍贯","民族","政治面貌","学历","工作单位",
                  "手机号码","户籍","居住地址","车牌号","户主","是否常住人口","是否重点人口",
                  "重点人口类型","是否自住型商品房","住房购买日期","备注","婚姻状况"]
    S_Headings = ["姓名","性别","身份证","年龄","政治面貌","学生证","学校","学院","专业","年级",
                  "班级","宿舍","宿舍盒子编码","籍贯","家庭地址"]
    
    Type_df = ReadType(conn) 
    for x,y in dic.items():
        Room_df = ReadHouseInfo(x,conn)
        Person_df = ReadPersonInfo(x,y,conn)
            
        main_dir=os.path.join(maindir,y)
        os.chdir(main_dir)
        writer = pd.ExcelWriter(x + '人口信息录入表.xlsx',engine='xlsxwriter')
        workbook = writer.book
                
        Type_df.to_excel(writer,'TypeRef',index = False,startrow = 1)
        T_worksheet = writer.sheets['TypeRef']
        StandardFormat(workbook,T_worksheet,T_Headings,Type_df)
                
        Room_df.to_excel(writer,'RoomRef',index = False,startrow = 1)
        R_worksheet = writer.sheets['RoomRef']
        StandardFormat(workbook,R_worksheet,R_Headings,Room_df)
                
        if y == "贵安数字经济产业园" or y == "摆井安置小区" or y == "翁岩安置小区" or y == "大坝井安置房":
            Person_df.to_excel(writer,'PeopleInfo',index = False,startrow = 1)
            P_worksheet = writer.sheets['PeopleInfo']
            StandardFormat(workbook,P_worksheet,P_Headings,Person_df)
        else:
            Person_df.to_excel(writer,'StudentInfo',index = False,startrow = 1)
            S_worksheet = writer.sheets['StudentInfo']
            StandardFormat(workbook,S_worksheet,S_Headings,Person_df)
                    
        workbook.close    
        writer.save()
        os.chdir(maindir)




def Main():  
    dic = OrderedDict()
    main_dir = r'D:\Xinge_Techonology\Temp_Working_Zone\贵安大学城人口信息整理'
    conn = pymssql.connect(server='192.168.17.8', user='sa', password='Xinge2018', database='GuiYang_UniversityTown_New')
    V_sql = "Select Name from T_Village"
    File_df = pd.read_sql_query(V_sql,conn)
    for i in File_df.index:
        dic[i] = File_df['Name'][i]
    MakeDirs(dic,main_dir)
    
    B_sql = "Select AreaName,Address From T_Building"
    A_df = pd.read_sql_query(B_sql,conn)
    AN = OrderedDict()
    for i in A_df.index:
        AN[A_df['Address'][i]] = A_df['AreaName'][i]
    
    Exc = MakeExcel(AN,main_dir,conn)




if __name__ == '__main__':
    Main()

