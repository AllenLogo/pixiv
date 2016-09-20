#-*- coding:utf-8 -*-

import http.cookiejar as cookielib
import os.path
import requests
from bs4 import BeautifulSoup


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
login_data = {
        'mode': 'login',
        'pass': '159478632',
        'pixiv_id': 'allenlogo',
        'return_to': '/',
        'skip': 1
    }
#session
session = requests.session()
#cookie
session.cookies = cookielib.LWPCookieJar(filename=cookiefile)



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
        HTMLPage = session.get(url, headers=headers)
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("GET", value))

#POST请求
def POST(url, postData={}, headers=None):
    global session, header
    try:
        if headers is None:
            headers = header
        HTMLPage = session.post(url, data=postData, headers=headers).text
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("POST", value))