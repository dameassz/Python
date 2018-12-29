
# coding: utf-8

# In[8]:


import ReadBoxCode as rc

from comtypes.client import CreateObject
from comtypes.gen import TerraExplorerX as TE

from collections import OrderedDict

from sqlalchemy import create_engine, MetaData, Table, Column
from sqlalchemy.exc import IntegrityError, DatabaseError


# In[11]:


def main():
    flypath = r"D:\Xinge_Techonology\Temp_Working_Zone\520111103213020003.fly"
    te = CreateObject("TerraExplorerX.TerraExplorer.1")
    sgworld = CreateObject("TerraExplorerX.SGWorld66.1")
    te.Load(flypath)    
    protree = sgworld.ProjectTree
    
    bcode = r"520111103213020003"
    
#    rootId = protree.RootId
    rootId = protree.FindItem(bcode)
    PDG = rc.ReadProjectTree(protree, rootId)
    args = (protree, PDG, rootId)
    #RepresentTreeStructure(*args) 
    swrong = rc.CheckTreeStructure(*args, 4)
    print(rc.CheckCodeLength(*args, 18, 4, 4, 4))
    PWDG = rc.ConstructWeightDiGraph(*args)
    print(rc.CheckDulplicatedObject(PWDG))
    #print(PWDG.node(data=True))
    
    housecode = OrderedDict()
    housecode = rc.GetAllBox(PWDG)
    #print(housecode)

    houses_obj = { hcode : protree.GetObject(h).QueryInterface(TE.ITerrain3DPolygon66) for h, hcode in housecode.items()}
    hvalues = [
    {
        'Geometry' : hobj.Geometry.Wks.ExportToWKT(),
        'Height' : hobj.Height,
        'Code' : hcode,
        'Longitude' : hobj.Position.X,
        'Latitude' : hobj.Position.Y,
        'Altitude' : hobj.Position.Altitude
    }
    for hcode, hobj in houses_obj.items()
    ]
    print(hvalues)
    


# In[12]:


if __name__ == '__main__':
    main()


# In[1]:


import sys 


# In[4]:


sys.path


# In[3]:


sys.path.append(r'D:\Xinge_Techonology\Data_Operation\Scripts\Python_Script')


# In[ ]:


metadata = MetaData()
engine = create_engine('mssql+pymssql://sa:Xinge2018@192.168.17.8:1433/GuiYang_UniversityTown')
HouseBox = Table('T_HouseBox', metadata,
            extend_existing=True,
            autoload=True,
            autoload_with=engine)
    rc.InsertData(engine, HouseBox, hvalues)

