#!/usr/bin/env python
#-*- coding:utf-8 -*-


"""
@version: 1.0
@author: allenlogo
@contact: allenlogotk@gmail.com
@software: PyCharm
@file: pixiv.py
@time: 2016/11/28 12:46
"""

#三方库
import os
import re
import json
import copy
import time
from functools import wraps
from PIL import Image
#私有库
from utils import ConfUtils
from mysql.MyDB import ImgDB, TagsDB
from utils import HttpUtils, FileUtils, HTMLUtils

indexurl = ConfUtils.cf.get("url", "indexurl")
loginurl = ConfUtils.cf.get("url", "loginurl")
login_data = eval(ConfUtils.cf.get("login", "login_data"))
memberillusturlModel = ConfUtils.cf.get("url", "memberillusturlModel")
work_workmultipleurl = ConfUtils.cf.get("url", 'work_workmultipleurl')
number = int(ConfUtils.cf.get("download", "number"))
portraitDir = ConfUtils.cf.get("dir", "portraitDir")

mytags = ['MHX', 'モンハン', 'モンスターハンタースピリッツ']
pixivListNew = []
pixivListOld = []

def getSoup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resp = HttpUtils.GET(args[0])
        soup = HTMLUtils.get_soup(resp.text)
        result = func(*args, soup=soup, **kwargs)
        resp.close()
        return result
    return wrapper

@getSoup
def getpost_key(url, soup=None):
    return soup.find("input", attrs={"name": "post_key"})['value']

def login():
    post_key = getpost_key(loginurl)
    if post_key is None:
        print("find post_key error")
        return False
    login_data['post_key'] = post_key
    data = json.loads(HttpUtils.POST("https://accounts.pixiv.net/api/login?lang=zh", postData=login_data).text)
    if data['error'] is False:
        return True


def scanningMemberillust(pid):
    print("[%s] start..." % pid)
    getMemberillustV2(memberillusturlModel.replace("{id}", pid).replace("{page}", "1"), pid, 1)
    print("[%s] end..." % pid)

@getSoup
def getMemberillustV2(memberillusturl, pid, page, soup=None):
    '''
    work_work-单图,work_workugoku-illust-动图，work_workmultiple-多图,work_workmangamultiple-类似漫画
    :param imgDB:
    :param memberillusturl:
    :param pid:
    :param page:
    :param soup:
    :return:
    '''
    if page > getmemberillustpageCount(soup):
        return
    illusts = soup.find('ul', attrs={'class': '_image-items'})
    for illust in illusts.findAll('li'):
        try:
            illustA = illust.find('a')
            imgPid = getPid(illustA['href'])
            imgClasss = "".join(illustA['class'])
            #if len(imgDB.find(author=pid, pid=imgPid)) != 0: continue
            if imgClasss == 'work_work':
                work_workStep1("%s%s" % (indexurl, illustA['href']), pid, imgPid)
            elif imgClasss == 'work_workmultiple':
                work_workmultipleStep1("%s%s" % (indexurl, illustA['href']), pid, imgPid)
        except Exception as error:
            print("Error", error)
    page += 1
    getMemberillustV2(memberillusturlModel.replace("{id}", pid).replace("{page}", str(page)), pid, page)

def getPid(Str):
    result = re.compile(r"illust_id=[0-9]*").findall(Str)
    if len(result) == 1:
        return result[0].replace("illust_id=", "")
    else:
        raise Exception("id error")

def getmemberillustpageCount(soup):
    '''获取作品'''
    if soup.find('ul', attrs={'class': 'page-list'}) is not None:
        liList = soup.find('ul', attrs={'class': 'page-list'}).findAll('li')
        return int(liList[len(liList)-1].text)
    return 1

@getSoup
def work_workStep1(url, pid, imgPid, soup=None):
    imgName = getName(soup)
    imgTags = getTags(soup)
    img = soup.find('img', attrs={'alt': imgName, 'class': 'original-image'})
    imgSrc = img['data-src']
    headers = copy.copy(HttpUtils.downLoadHead)
    headers[':path'] = imgSrc[imgSrc.find('img-master')-1:]
    headers['referer'] = headers['referer'].replace("{id}", pid).replace('{imgid}', imgPid)
    downLoad(imgSrc, portraitDir + FileUtils.getfile(imgSrc), headers)

@getSoup
def work_workmultipleStep1(memberillusturl, pid, imgPid, soup=None):
    tags = getTags(soup)
    imgName = getName(soup)
    tmp = [val for val in tags if val in mytags]
    if len(tmp) != 0:
        work_workmultipleStep2(work_workmultipleurl.replace("{imgid}", getPid(memberillusturl)), pid, imgPid)

@getSoup
def work_workmultipleStep2(memberillusturl, pid, imgPid, soup=None):
    for a in soup.findAll('a', attrs={'class': 'full-size-container _ui-tooltip'}):
        work_workmultipleStep3("%s%s" % (indexurl, a['href']), pid, imgPid)

@getSoup
def work_workmultipleStep3(memberillusturl, pid, imgPid, soup=None):
    img = soup.find('img')
    imgSrc = img['src']
    headers = copy.copy(HttpUtils.downLoadHead1)
    headers['Referer'] = memberillusturl
    downLoad(imgSrc, portraitDir+FileUtils.getfile(imgSrc), headers)

def downLoad(src, imgFile, headers):
    resp1 = HttpUtils.GET(src, Myheaders=headers)
    FileUtils.saveFile_img(imgFile, resp1)
    resp1.close()
    time.sleep(1)
    f = open(imgFile, "rb")
    im = Image.open(f)
    f.close()
    x, y = im.size
    print({'imagename': FileUtils.getfile(imgFile), 'image_x': x, 'image_y': y})

def getTags(soup):
    Tags = []
    tags = soup.find('span', attrs={'class': 'tags-container'}).find('ul').findAll('li')
    for tag in tags:
        Tags.append(tag.find('a', attrs={'class': 'text'}).text)
    return Tags

def getName(soup):
    name = soup.find('div', attrs={'class': 'ui-expander-target'})
    if hasattr(name, 'find'):
        name = name.find('h1', attrs={'class': 'title'})
    else:
        name = soup.find('div', attrs={'class': '_unit _work-detail-unit'}).find('h1', attrs={'class': 'title'})
    return name.text