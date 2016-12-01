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

downLoadHead = {
':authority': 'i.pximg.net',
':method': 'GET',
':path': '/img-master/img/2016/10/01/21/50/20/59256176_p0_master1200.jpg',
':scheme': 'https',
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'accept-encoding': 'gzip, deflate, sdch, br',
'accept-language': 'zh-CN,zh;q=0.8',
'cache-control': 'no-cache',
'pragma': 'no-cache',
'referer': 'http://www.pixiv.net/user/{id}/illust/{imgid}',
'upgrade-insecure-requests': 1,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

downLoadHead1 = {
'Accept': 'image/webp,image/*,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate, sdch',
'Accept-Language': 'zh-CN,zh;q=0.8',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Cookie': 'p_ab_id=8; uaid=10e76aae31756868b6d246ea122fcaf3; device_token=6fab08f0d90ad1e1f5145fd36a82b0dc; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; _ga=GA1.2.58026910.1473640694; PHPSESSID=20249597_87941cf0015ba99d16ae5c29e8237403; __utma=235335808.58026910.1473640694.1480403560.1480407456.44; __utmb=235335808.3.10.1480407456; __utmc=235335808; __utmz=235335808.1480384421.39.10.utmcsr=cloud.mokeyjay.com|utmccn=(referral)|utmcmd=referral|utmcct=/pixiv/; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=20249597=1',
'Host': 'i3.pixiv.net',
'Pragma': 'no-cache',
'Referer': 'http://www.pixiv.net/member_illust.php?mode=manga_big&illust_id={imgid}&page=0',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}
#session
session = requests.session()

#GET请求
def GET(url, Myheaders=headerModel):
    try:
        HTMLPage = session.get(url, headers=Myheaders, timeout=1000)
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("GET", value))

#POST请求
def POST(url, postData={}, headers=headerModel):
    try:
        HTMLPage = session.post(url, data=postData, headers=headers, timeout=1000)
        return HTMLPage
    except Exception as value:
        print("%s_%s" % ("POST", value))