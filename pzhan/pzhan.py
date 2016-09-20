#-*- coding:utf-8 -*-

import http.cookiejar as cookielib
import os.path
import time
import requests
from bs4 import BeautifulSoup

from mysql.MyDB import Up as UpDB
#-----基本配置-----#

#文件地址
basePath = os.path.dirname(__file__)
#cookie保存地址
cookiefile = os.path.join(basePath + '/../conf/cookie/cookies_pixiv')
#请求头
header = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'https://www.pixiv.net/login.php?return_to=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
#session
session = requests.session()
#cookie
session.cookies = cookielib.LWPCookieJar(filename=cookiefile)

#-----基本配置-----#

#-----函数-----#

#获取网页内容分析对象
def get_soup(htmldata):
    soup = BeautifulSoup(htmldata, "html.parser", exclude_encodings="utf-8")
    return soup

#GET请求
def GET(url, headers=None):
    global session, header
    try:
        if headers is None:
            headers = header
        HTMLPage = session.get(url, headers=headers).text
        return HTMLPage
    except Exception as value:
        print(value)

#POST请求
def POST(url, postData={}, headers=None):
    global session, header
    try:
        if headers is None:
            headers = header
        HTMLPage = session.post(url, data=postData, headers=headers).text
        return HTMLPage
    except Exception as value:
        print(value)

#登陆
def login():
    global session, header
    login_data = {
        'mode': 'login',
        'pass': '159478632',
        'pixiv_id': 'allenlogo',
        'return_to': '/',
        'skip': 1
    }
    if os.path.isfile(cookiefile):
        session.cookies.load(cookiefile, ignore_discard=True, ignore_expires=True)
    else:
        POST("https://www.pixiv.net/login.php", postData=login_data, headers=header)
        session.cookies.save()


def downLoad_HTMLPage(url):
    global session, header
    try:
        with open("%s.txt" % url.split("?id=", 1)[1],"w",encoding="utf-8") as f:
            f.write(GET(url))
    except Exception as value:
        print(value)

def downLoad_HTMLImg(url):
    global session, header
    try:
        with open("p11.jpg", 'wb') as f:
            resp1 = session.get(url, headers=headers)
            for chunk in resp1.iter_content(chunk_size=512):
                f.write(chunk)
            resp1.close()
    except Exception as value:
        print(value)

def saveUp(url):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    soup = get_soup(GET(url))
    table = soup.find('table', attrs={'class': "ws_table"})
    try:
        up = UpDB(pid=url.split("?id=", 1)[1], name=table.findAll('tr')[0].findAll('td')[1].text, url=url, recdate=date, padate=date)
        up.save()
    except Exception as value:
        print(value)


bookmarkurl = 'http://www.pixiv.net/bookmark.php?type=user&id={id}&rest=show&p={page}'
def getBookMark(url):
    pass

if __name__ == '__main__':
    login()
    saveUp('http://www.pixiv.net/member.php?id=6815602')
