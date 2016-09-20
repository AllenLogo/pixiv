#coding:UTF-8

import urllib
import urllib2
import cookielib

url = 'https://www.pixiv.net/login.php'
filename = 'cookie.txt'

cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
#build_opener函数是用来自定义opener对象的函数

login_data = urllib.urlencode({
    'mode': 'login',
    'pass': '159478632',#你的账号密码
    'pixiv_id': 'allenlogo',#你的pixivid
    'return_to': '/',
    'skip': 1
    })
#这个是p站的登陆信息
header = {
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Referer':'https://www.pixiv.net/login.php?return_to=0',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:45.0) Gecko/20100101 Firefox/45.0'
    }
#登陆所使用的请求头信息
request = urllib2.Request(
    url,
    data = login_data,
    headers = header)

login_pixiv = opener.open(request)
#利用前面的请求头信息与cookie信息进行登陆

cookie.save(ignore_discard = True , ignore_expires = True)
#登陆成功后进入收藏界面
bookmark_url = 'http://www.pixiv.net/member.php?id=6815602'

login_pixiv =opener.open(bookmark_url)
page = login_pixiv.read()

file_html = open('pixiv-1.html','w')
file_html.write(page)
file_html.close()

print(page)  #其实这个print我只是想看看是否登陆成功