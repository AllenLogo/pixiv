#-*- coding:utf-8 -*-

import os.path
from functools import wraps


def createbasePath(file):
    return os.path.dirname(file)

def joinPath(filePath1, filePath2):
    return os.path.join("%s%s" % (filePath1, filePath2))

def checkFile(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if os.path.isfile(args[0]):
            print("%s文件已存在" % args[0])
        else:
            result = func(*args, **kwargs)
            return result
    return wrapper

@checkFile
def saveFile_img(imgFilePath, sourceImgFile):
    with open(imgFilePath, 'wb') as f:
        for chunk in sourceImgFile.iter_content(chunk_size=512):
            f.write(chunk)