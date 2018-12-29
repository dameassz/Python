# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import os, sys

from comtypes.client import CreateObject
from comtypes.gen import TerraExplorerX as TE

import networkx as nx
from pprint import pprint

from collections import OrderedDict
	
def ReadProjectTree(projectTree, rootId, PDG=nx.DiGraph()):
    PDG.add_node(rootId)
    nextItem = projectTree.GetNextItem(rootId, 11)
    while nextItem != '':
        PDG.add_edge(rootId, nextItem)
        nextItem = projectTree.GetNextItem(nextItem, 13)
    for upperNode, lowerNode in PDG.edges(rootId):
        if projectTree.IsGroup(lowerNode):
            PDG = ReadProjectTree(projectTree, lowerNode, PDG)
    return PDG

def RepresentTreeStructure(projectTree, PDG, rootId, depth=0):
    if rootId == '':
        print('ProjectTreeRoot')
    else:
        print('-**-'*depth + projectTree.GetItemName(rootId))
    for upperNode, lowerNode in PDG.edges(rootId):
        depth += 1
        if projectTree.IsGroup(lowerNode):
            RepresentTreeStructure(projectTree, PDG, lowerNode, depth)
        else:
            print('-**-'*depth + projectTree.GetItemName(lowerNode))
        depth -= 1
    

def GetPathByDepth(projectTree, objectId, depth, totalDepth):
    """
    此函数用于根据工程树目录深度组成路径
    """
    itemNameList = []    
    while totalDepth >= depth:
        itemNameList.append(projectTree.GetItemName(objectId).replace(' ', ''))
        objectId = projectTree.GetNextItem(objectId, 15)
        depth += 1
    itemNameList.reverse()
    return ''.join(itemNameList)
    
        
def CheckTreeStructure(projectTree, PDG, rootId, depth):
    """
    检查工程树结构，仅适用于检查盒子的层级结构
    rootId不能是工程树的RootId
    """        
    if rootId == '':
        return
#        sys.exit('检查入口ID值为空！')
    wrongBox=[]
    totalDepth = depth
    nodeList = [rootId,]
    while depth > 0:
        if depth == 1:
            for n in nodeList:
                if projectTree.IsGroup(n):
                    wrongBox.append(GetPathByDepth(projectTree, n, depth, totalDepth))
        else:
            for n in nodeList:
                if projectTree.IsGroup(n) != True:
                    wrongBox.append(GetPathByDepth(projectTree, n, depth, totalDepth))  
            nodeList = [lowerNode for rid in nodeList for upperNode, lowerNode in PDG.edges(rid)]
        depth -= 1
    return wrongBox

def CheckCodeLength(projectTree, PDG, rootId, *length):
    """
    用于检查各层级编码长度，检查此项前应先检查树形结构的深度是否满足要求
    rootId不能是工程树的RootId
    """
    if rootId == '':
        return 
    wrongBox = []
    depth = len(length) 
    totalDepth = depth
    nodeList = [rootId,]
    while depth > 0:
        for n in nodeList:
            if len(projectTree.GetItemName(n)) != length[len(length)-depth]:
                wrongBox.append(GetPathByDepth(projectTree, n, depth, totalDepth))
        
        nodeList = [lowerNode for rid in nodeList for upperNode, lowerNode in PDG.edges(rid)]
        depth -= 1
    return wrongBox

def ConstructWeightDiGraph(projectTree, PDG, rootId):
    depth = 1
    nodeList = [rootId,]
    while len(nodeList) > 0:
        for n in nodeList:
            if projectTree.IsGroup(n):
                PDG.node[n]['ObjectType'] = 0
            else:
                PDG.node[n]['ObjectType'] = projectTree.GetObject(n).ObjectType
            PDG.node[n]['Path'] = GetPathByDepth(projectTree, n, 1, depth)
        nodeList = [lowerNode for rid in nodeList for upperNode, lowerNode in PDG.edges(rid)] 
        depth += 1
    return PDG

def CheckDulplicatedObject(PWDG):
    """
    参数PWDG是具有‘ObjectType’和‘Path’参数的节点构成的有向图
    """
    objs = [ PWDG.node[n] for n in PWDG.nodes ]
    rightObjs = []
    dulpObjs = []    
    for od in objs:
        for rd in rightObjs:
            if od['ObjectType'] == rd['ObjectType'] and od['Path'] == rd['Path']:
                dulpObjs.append(od)
        else:
            rightObjs.append(od)
    return dulpObjs

def GetAllBox(PWDG):
    nodes_p=dict([((u),d['Path']) for u,d in PWDG.nodes(data=True)])
    i = 0
    code = OrderedDict()
    houses = OrderedDict()
    for z,c in nodes_p.items():
        code[z] = c
    
    for key,value in code.items():
        if len(value) == 30:
            houses[key] = value
    return houses
	
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
