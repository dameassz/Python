
# coding: utf-8

# In[1]:


import os, sys
from pprint import pprint
from collections import namedtuple, OrderedDict


# In[16]:


def MakeDirs(dic, maindir):
    os.makedirs(maindir)
    for p, c in dic.items():
        if type(c) is list:
            if len(c) != 0:
                for i in c:
                    os.makedirs(os.path.join(maindir, p, i))
            else:
                os.mkdir(os.path.join(maindir, p))
        elif type(c) is dict:
            MakeDirs(c, maindir=os.path.join(maindir, p))
        else:
            print('No'*20)


# In[17]:


if __name__ == '__main__':

	main_dir = 'D:\Xinge_Techonology'

	cascade_dict = {
		"Layer" : {
			"MeshLayer" : ["3DML", "OSGB", "VTK"],
			"TerrainLayer" : ["MPT",],
			"FeatureLayer" : ["SHP", "KML", "SQLite", "CSV", "GeoJson", "XML"],
			"ImageLayer" : ["GIFF", "Elevation"],
			"Model" : {
				"Image" : ["PNG", "JPG"],
				"3DModel" : ["XPL", "3DS"]
			},
			"CAD" : []        
		},
		"Data_Operation" : {
			"Database" : ["SQLServer", "Postgre", "SQLite", "MySQL"],
			"Scripts" : ["Python_Script", "Shell_Script", "SQL_Script"],
			"XLS" : [],
			"TXT" : []
		},
		"Operation" : {
			"Server" : ["ALi_Cloud", "TC_Cloud", "Inner_Using", "Project_Using"],
			"SVN&Github" : ["SVN", "Github"],
			"Network" : [],
			"Deploy" : [],
			"DNS_Admin" : [],
			"OS" : [],
			"Develop_Platform" : ["WeiXin_Develop_Platform"]
		},
		"DPT_Document" : ["Admin_DPT" , "Research_DPT" , "Project_ DPT", "DataCenter"]
	}
    
	MakeDirs(cascade_dict, maindir=main_dir)


# In[18]:


help(os.path.join)

