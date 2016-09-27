#-*- coding:utf-8 -*-

#三方库
import http.cookiejar as cookielib
import requests
#私有库
from .import FileUtils

#文件地址
basePath = FileUtils.getpath()
#cookie保存地址
cookiefile = FileUtils.joinPath(FileUtils.getdir(basePath), 'conf\cookie\cookies_pixiv')
#请求头
headerModel = {
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Referer': 'https://www.pixiv.net/login.php?return_to=0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}
#session
session = requests.session()
#cookie
session.cookies = cookielib.LWPCookieJar(filename=cookiefile)

def loadCookies(cookiefile=cookiefile):
    session.cookies.load(cookiefile, ignore_discard=True, ignore_expires=True)

def saveCookies(cookiefile=cookiefile):
    session.cookies = cookielib.LWPCookieJar(filename=cookiefile)
    session.cookies.save()

#GET请求
def GET(url, headers=headerModel):
    try:
        HTMLPage = session.get(url, headers=headers, timeout=600)
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("GET", value))

#POST请求
def POST(url, postData={}, headers=headerModel):
    try:
        HTMLPage = session.post(url, data=postData, headers=headers, timeout=600)
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("POST", value))