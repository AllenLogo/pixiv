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

import sys
sys.path.append("..")
import re
import json
import copy
import time
from functools import wraps
from PIL import Image
from utils import ConfUtils
from utils import HttpUtils, FileUtils, HTMLUtils

indexurl = ConfUtils.cf.get("url", "indexurl")
loginurl = ConfUtils.cf.get("url", "loginurl")
login_data = eval(ConfUtils.cf.get("login", "login_data"))
memberillusturlModel = ConfUtils.cf.get("url", "memberillusturlModel")
work_workmultipleurl = ConfUtils.cf.get("url", 'work_workmultipleurl')
bookmarkuserurlModel = ConfUtils.cf.get("url", "bookmarkuserurlModel")
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
    work_work-one img,work_workugoku-illust-active img，work_workmultiple-more img,work_workmangamultiple-imgs
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
            if imgClasss == 'work_work':
                work_workStep1("%s%s" % (indexurl, illustA['href']), pid, imgPid)
            elif imgClasss == 'work_workmultiple':
                work_workmultipleStep1("%s%s" % (indexurl, illustA['href']), pid, imgPid)
        except Exception as error:
            print("getMemberillustV2 function Error:", str(error))
    page += 1
    getMemberillustV2(memberillusturlModel.replace("{id}", pid).replace("{page}", str(page)), pid, page)

def getPid(Str):
    result = re.compile(r"illust_id=[0-9]*").findall(Str)
    if len(result) == 1:
        return result[0].replace("illust_id=", "")
    else:
        raise Exception("id error")

def getmemberillustpageCount(soup):
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
    headers[':path'] = imgSrc[imgSrc.find('.pixiv.net/')+10:]
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
    try:
        HTMLUtils.downLoad_HTMLImg(src, imgFile, headers=headers)
        im = Image.open(imgFile)
        x, y = im.size
        print({'imagename': FileUtils.getfile(imgFile), 'image_x': x, 'image_y': y})
    except Exception as error:
        print("downLoad function error:" + error)
        raise

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

def getbookmarkuserpageCount(soup):
    if soup.find('div', attrs={'class': 'pages'}) is not None and soup.find('div', attrs={'class': 'pages'}).find('ol') is not None:
        liList = soup.find('div', attrs={'class': 'pages'}).find('ol').findAll('li')
        return int(liList[len(liList)-2].text)
    return 1

@getSoup
def getBookMarkV2(bookmarkurl, pid, page, bookMark=[], soup=None):
    if page > getbookmarkuserpageCount(soup):
        return
    userList = soup.find('div', attrs={'class': 'members'}).find('ul')
    for userLi in userList.findAll('li'):
        userA = userLi.find('a', attrs={'class': "ui-profile-popup"})
        bookMark.append(userA['data-user_id'])
    page += 1
    getBookMarkV2(bookmarkuserurlModel.replace("{id}", pid).replace("{page}", "1"), pid, page)

def scanningBookMark(pid):
    bookMarks = []
    getBookMarkV2(bookmarkuserurlModel.replace("{id}", pid).replace("{page}", "1"), pid, 1, bookMark=bookMarks)
    newBookMarks = [bookMark for bookMark in bookMarks if bookMark not in pixivListNew and bookMark not in pixivListOld]
    pixivListNew.extend(newBookMarks)

def start():
    while len(pixivListNew) != 0:
        if pixivListNew[0] in pixivListOld:
            del pixivListNew[0]
        else:
            pid = pixivListNew[0]
            scanningMemberillust(pid)
            # pixiv.pixivListOld.append(pid)
            del pixivListNew[0]
            # pixiv.scanningBookMark(pid)
        if int(time.strftime("%H", time.localtime())) <= 23:
            break

if __name__ == '__main__':
    if login() is True:
        pixivListNew.append("34637")
        start()
    else:
        print("Login error...")