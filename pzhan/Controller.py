#!/usr/bin/env python
#-*- coding:utf-8 -*-


"""
爬虫流程控制
@version: 1.0
@author: allenlogo
@contact: allenlogotk@gmail.com
@software: PyCharm
@file: Controller.py
@time: 2016/11/29 15:30
"""
import sys
sys.path.append("..")
import pixiv
import time


def start():
    while len(pixiv.pixivListNew) != 0:
        if pixiv.pixivListNew[0] in pixiv.pixivListOld:
            del pixiv.pixivListNew[0]
        else:
            pid = pixiv.pixivListNew[0]
            pixiv.scanningMemberillust(pid)
            # pixivListOld.append(pid)
            del pixiv.pixivListNew[0]
            #scanningBookMark(pid)
        if int(time.strftime("%H", time.localtime())) <= 23:
            break

if __name__ == '__main__':
    if pixiv.login() is True:
        pixiv.pixivListNew.append("34637")
        start()
    else:
        print("登陆失败")