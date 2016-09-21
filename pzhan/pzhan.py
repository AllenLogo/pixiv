#-*- coding:utf-8 -*-

import os.path
import time

from utils import HttpUtils, FileUtils
from mysql.MyDB import Up as UpDB


login_data = {
        'mode': 'login',
        'pass': '159478632',
        'pixiv_id': 'allenlogo',
        'return_to': '/',
        'skip': 1
    }

#登陆
def login():
    if os.path.isfile(HttpUtils.cookiefile):
        HttpUtils.loadCookies()
    else:
        HttpUtils.POST("https://www.pixiv.net/login.php", postData=login_data)
        HttpUtils.saveCookies()


def downLoad_HTMLPage(url, pid):
    try:
        HTML_page = HttpUtils.GET(url)
        with open("%s.txt" % pid, "w", encoding="utf-8") as f:
            f.write(HTML_page.text)
    except Exception as value:
        print(value)

def downLoad_HTMLImg(url, imgFile):
    try:
        imgFile = "%s.%s" % (imgFile, url[-3:])
        resp1 = HttpUtils.GET(url)
        FileUtils.saveFile_img(imgFile, resp1)
        resp1.close()
    except Exception as value:
        print("%s_%s" % ("downLoad_HTMLImg", value))

def saveUp(url):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    soup = HttpUtils.get_soup(HttpUtils.GET(url))
    table = soup.find('table', attrs={'class': "ws_table"})
    try:
        up = UpDB(pid=url.split("id=", 1)[1], name=table.findAll('tr')[0].findAll('td')[1].text, url=url, recdate=date)
        up.save()
    except Exception as value:
        print(value)

def saveUp(pid, name, url):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        up = UpDB(pid=pid, name=name, url=url, recdate=date)
        up.save()
    except Exception as value:
        print(value)

bookmarkurl = 'http://www.pixiv.net/bookmark.php?type=user&id={id}&rest=show&p={page}'


def getBookMark(bookmarkurlModel, pid, page):
    HTMLData = HttpUtils.GET(bookmarkurlModel.replace("{id}", pid).replace("{page}", page))
    soup = HttpUtils.get_soup(HTMLData.text)
    userList = soup.find('div', attrs={'class': 'members'}).find('ul')
    for userLi in userList.findAll('li'):
        userA = userLi.find('a', attrs={'class': "ui-profile-popup"})
        downLoad_HTMLImg(userA['data-profile_img'], userA['data-user_id'])
        #saveUp(userA['data-user_id'], userA['data-user_name'], "http://www.pixiv.net/%s" % userA['href'])
    return len(userList)

if __name__ == '__main__':
    login()
    page = 1
    userList = 48
    while userList == 48:
        userList = getBookMark(bookmarkurl, "6815602", str(page))
        page += 1
        print("已经扫描用户")