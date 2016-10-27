#-*- coding:utf-8 -*-

#三方库
import requests

#请求头
headerModel = {
    'Accept - Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
    'Referer': 'https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.14951'
}
#session
session = requests.session()

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