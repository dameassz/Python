# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 09:06:26 2018

@author: Administrator
"""
import os
from collections import OrderedDict
from comtypes.client import CreateObject

#flyDir = r"D:\XingeTech\Operation\DataOperation\Demo\HuaGuoYuan\FLY"
#flyName = r"test.FLY"
bcode = "52010241800314"
#flypath = os.path.join(flyDir, flyName)
flypath = "http://192.168.17.8/GuiYang_HGY/hgy.fly"

te = CreateObject("TerraExplorerX.TerraExplorer.1")
te.Load(flypath)

sgworld = CreateObject("TerraExplorerX.SGWorld66.1")
protree = sgworld.ProjectTree

bgroup = protree.FindItem(bcode)

units = OrderedDict()
wrongunits = []
floors = OrderedDict()
wrongfloors = []
houses = OrderedDict()
wronghouses = []

if bgroup != '':
    ugroup = protree.GetNextItem(bgroup, 11)
    while ugroup != '':
        ucode = bcode + protree.GetItemName(ugroup).replace(' ', '')
        if protree.IsGroup(ugroup) and ucode.isdigit() and len(ucode) == 16:
            if ucode not in units:
                units[ucode] = ugroup
            else:
                wrongunits.append(ucode)
            fgroup = protree.GetNextItem(ugroup, 11)
            while fgroup != '':
                fcode = ucode + protree.GetItemName(fgroup)
                if protree.IsGroup(fgroup) and fcode.isdigit() and len(fcode) == 20:
                    if fcode not in floors:
                        floors[fcode] = fgroup
                    else:
                        wrongfloors.append(fcode)
                    h = protree.GetNextItem(fgroup, 11)
                    while h != '':
                        hcode = fcode + protree.GetItemName(h)
                        if hcode not in houses:
                            houses[hcode] = {'box' : '', 'loc' : ''}
                            if protree.GetObject(h).ObjectType == 6:
                                if houses[hcode]['box'] == '':
                                    houses[hcode]['box'] = h
                                else:
                                    wronghouses.append(hcode)
                            elif protree.GetObject(h).ObjectType == 19:
                                if houses[hcode]['loc'] == '':
                                    houses[hcode]['loc'] = h
                                else:
                                    wronghouses.append(hcode)
                            else:
                                wronghouses.append(hcode)
                        else:
                            if protree.GetObject(h).ObjectType == 6:
                                if houses[hcode]['box'] == '':
                                    houses[hcode]['box'] = h
                                else:
                                    wronghouses.append(hcode)
                            elif protree.GetObject(h).ObjectType == 19:
                                if houses[hcode]['loc'] == '':
                                    houses[hcode]['loc'] = h
                                else:
                                    wronghouses.append(hcode)
                            else:
                                wronghouses.append(hcode)
                        h = protree.GetNextItem(h, 13)
                
                else:
                    wrongfloors.append(fcode)
                    
                fgroup = protree.GetNextItem(fgroup, 13)
        
        else:
            wrongunits.append(ucode)
            
        ugroup = protree.GetNextItem(ugroup, 13)
        

 


       
if __name__ == '__main__':
    print(wrongunits, wrongfloors, wronghouses)
#    print(units, floors, houses)
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                        
                    