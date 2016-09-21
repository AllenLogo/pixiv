#-*- coding:utf-8 -*-

import os.path
from functools import wraps

def getpath():
    return os.getcwd()

def getfile(path):
    return os.path.basename(path)

def getdir(path):
    return os.path.dirname(path)

def joinPath(*args):
    return os.path.join(*args)

def exists(path):
    return os.path.exists(path)

def isfile(filePath):
    return os.path.isfile(filePath)

def isdir(dirPath):
    return os.path.isdir(dirPath)

def checkFile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if exists(args[0]):
            print("%s文件已存在" % args[0])
        else:
            result = func(*args, **kwargs)
            return result
    return wrapper

def checkDir(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if exists(args[0]):
            print("%s文件夹已存在" % args[0])
        else:
            result = func(*args, **kwargs)
            return result
    return wrapper

@checkDir
def createdir(dirPath):
    os.makedirs(dirPath)

@checkFile
def saveFile_img(imgFilePath, sourceImgFile):
    with open(imgFilePath, 'wb') as f:
        for chunk in sourceImgFile.iter_content(chunk_size=512):
            f.write(chunk)