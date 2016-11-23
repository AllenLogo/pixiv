#-*- coding:utf-8 -*-

import sys
sys.path.append("..")
#三方库
from functools import wraps
from utils import HttpUtils, FileUtils, HTMLUtils
import json
#私有库
from utils import ConfUtils
from mysql.MyDB import ImgDB, TagsDB

indexurl = ConfUtils.cf.get("url", "indexurl")
loginurl = ConfUtils.cf.get("url", "loginurl")
memberurlModel = ConfUtils.cf.get("url", "memberurlModel")
bookmarkuserurlModel = ConfUtils.cf.get("url", "bookmarkuserurlModel")
memberillusturlModel = ConfUtils.cf.get("url", "memberillusturlModel")
bookmarkurlModel = ConfUtils.cf.get("url", "bookmarkurlModel")
mypixivurlModel = ConfUtils.cf.get("url", "mypixivurlModel")
portraitDir = ConfUtils.cf.get("dir", "portraitDir")
rootdata = ConfUtils.cf.get("dir", "rootdata")

login_data = eval(ConfUtils.cf.get("login", "login_data"))

mytags = ['MHX', 'モンハン', 'モンスターハンタースピリッツ']

pixivListNew = []
pixivListOld = []

def getSoup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            soup = HTMLUtils.get_soup(HttpUtils.GET(args[0]).text)
            result = func(*args, soup=soup, **kwargs)
            return result
    return wrapper

def getError(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as value:
                print("函数：[%s]参数args：[%s]参数kwargs：[%s]异常：[%s]" % (func.__name__, args, kwargs, value))
    return wrapper

@getError
@getSoup
def getpost_key(url, soup=None):
    return soup.find("input", attrs={"name": "post_key"})['value']

@getError
def login():
    post_key = getpost_key(loginurl)
    if post_key is None:
        print("获取post_key失败")
        return False
    login_data['post_key'] = post_key
    data = json.loads(HttpUtils.POST("https://accounts.pixiv.net/api/login?lang=zh", postData=login_data).text)
    if data['error'] is False:
        return True

#提取用户关注
@getError
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

#扫描用户
@getError
def scanningBookMark(pid):
    print("获取用户[%s]关注开始" % pid)
    bookMarks = []
    getBookMarkV2(bookmarkuserurlModel.replace("{id}", pid).replace("{page}", "1"), pid, 1, bookMark=bookMarks)
    print("获取用户[%s]关注[%d]结束" % (pid, len(bookMarks)))
    newBookMarks = [bookMark for bookMark in bookMarks if bookMark not in pixivListNew and bookMark not in pixivListOld]
    print("新增扫描用户[%d]" % len(newBookMarks))
    pixivListNew.extend(newBookMarks)

@getError
def getmemberillustpageCount(soup):
    '''获取作品'''
    if soup.find('ul', attrs={'class': 'page-list'}) is not None:
        liList = soup.find('ul', attrs={'class': 'page-list'}).findAll('li')
        return int(liList[len(liList)-1].text)
    return 1

@getError
def getbookmarkuserpageCount(soup):
    if soup.find('div', attrs={'class': 'pages'}) is not None and soup.find('div', attrs={'class': 'pages'}).find('ol') is not None:
        liList = soup.find('div', attrs={'class': 'pages'}).find('ol').findAll('li')
        return int(liList[len(liList)-2].text)
    return 1

#扫描用户作品
@getError
def scanningMemberillust(pid):
    print("扫描用户[%s]作品开始" % pid)
    memberillust = []
    getMemberillustV2(memberillusturlModel.replace("{id}", pid).replace("{page}", "1"), pid, 1, memberillust=memberillust)
    print("扫描用户[%s]作品[%d]结束" % (pid, len(memberillust)))
    imgs = ImgDB()
    imgList = [img.url for img in imgs.find(author=pid)]
    downLoadURL = [url for url in memberillust if url not in imgList]
    for url in downLoadURL:
        checkMemberillust(url, pid)


@getError
@getSoup
def getMemberillustV2(memberillusturl, pid, page, memberillust=[], soup=None):
    if page > getmemberillustpageCount(soup):
        return
    illusts = soup.find('ul', attrs={'class': '_image-items'})
    for illust in illusts.findAll('li'):
        illustA = illust.find('a')
        memberillust.append("%s%s" % (indexurl, illustA['href']))
    page += 1
    getMemberillustV2(memberillusturlModel.replace("{id}", pid).replace("{page}", str(page)), pid, page, memberillust=memberillust)

#读取作品图片，标签
@getSoup
@getError
def checkMemberillust(memberillusturl, pid, soup=None):
    #读取标签
    tags = getTags(soup)
    tmp = [val for val in tags if val in mytags]
    if len(tmp) != 0:
        img = soup.find('div', attrs={'class': '_layout-thumbnail ui-modal-trigger'})
        if img:
            imgFile = FileUtils.joinPath(portraitDir, FileUtils.getfile(img['src']))
            if FileUtils.exists(imgFile):
                print("文件已存在[%s]" % imgFile)
            else:
                print("开始下载图片[%s]" % imgFile)
                HTMLUtils.downLoad_HTMLImg(img.find('img')['src'], imgFile)
                print("下载图片[%s]结束" % imgFile)
        else:
            img = soup.find('div', attrs={'class': 'works_display'})
            if img.find('a', attrs={'class': r' _work multiple '}):
                img1 = img.find('a', attrs={'class': r' _work multiple '})
            if img.find('a', attrs={'class': r' _work manga multiple '}):
                img1 = img.find('a', attrs={'class': r' _work manga multiple '})
            if img1 is not None:
                checkMemberillust_medium("%s%s%s" % (indexurl, '/', img1['href']), pid, img1['href'].split('=', 2)[2])

#读取画集
@getError
@getSoup
def checkMemberillust_medium(memberillusturl, pid, medium_id, soup=None):
    sections = soup.find('section', attrs={'class': 'manga'})
    for section in sections.findAll('div', attrs={'class': 'item-container'}):
        img = section.find('a', attrs={'class': "full-size-container _ui-tooltip"})
        HTMLData = HttpUtils.GET("%s%s"% (indexurl, img['href']))
        soup = HTMLUtils.get_soup(HTMLData.text)
        img = soup.find('img')
        imgFile = FileUtils.joinPath(portraitDir, FileUtils.getfile(img['src']))
        if FileUtils.exists(imgFile):
            print("文件已存在[%s]" % imgFile)
        else:
            print("开始下载图片[%s]" % imgFile)
            HTMLUtils.downLoad_HTMLImg(img['src'], imgFile)
            print("下载图片[%s]结束" % imgFile)

def getTags(soup):
    Tags = []
    tags = soup.find('span', attrs={'class': 'tags-container'}).find('ul')
    for tag in tags:
        Tags.append(tag.find('a', attrs={'class': 'text'}).text)
    return Tags.sort(reverse=True)

def start():
    while len(pixivListNew) != 0:
        if pixivListNew[0] in pixivListOld:
            del pixivListNew[0]
        else:
            pid = pixivListNew[0]
            scanningMemberillust(pid)
            # pixivListOld.append(pid)
            del pixivListNew[0]
            #scanningBookMark(pid)

if __name__ == '__main__':
    if login() is True:
        pixivListNew.append("34637")
        start()
    else:
        print("登陆失败")