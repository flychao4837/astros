#!/usr/bin/python
# coding=UTF-8
import os
import datetime

#获取文件根路径、相对路径

curFileWorkPath = os.getcwd()
filePath = os.path.split( curFileWorkPath )
curRootPath =filePath[0]
dataRootPath = curRootPath+'\data'
logRootPath = curRootPath+'\log'
htmlRootPath = curRootPath+'\html'
taskRootPath = curRootPath+'\task'

#创建文件根目录
def creatRootDirectories():
    if os.path.isdir(dataRootPath):
        pass
    else:
        os.mkdir(dataRootPath)

    if os.path.isdir(logRootPath):
        pass
    else:
        os.mkdir(logRootPath)

    if os.path.isdir(htmlRootPath):
        pass
    else:
        os.mkdir(htmlRootPath)