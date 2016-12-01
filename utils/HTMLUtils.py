# -*- coding:utf-8 -*-

#三方库
from bs4 import BeautifulSoup
#私有库
from .import HttpUtils, MyException, FileUtils

#获取网页内容分析对象
@MyException.raiseException
def get_soup(htmldata):
    return BeautifulSoup(htmldata, "html.parser", exclude_encodings="utf-8")

#获取页面流
@MyException.raiseException
def get_HTMLPage(url):
    return HttpUtils.GET(url)

#下载页面
@MyException.raiseException
def downLoad_HTMLPage(url, pid):
    HTML_page = HttpUtils.GET(url)
    with open("%s.txt" % pid, "w", encoding="utf-8") as f:
        f.write(HTML_page.text)

# 获取图片流
@MyException.raiseException
def downLoad_HTMLImg(url):
    return HttpUtils.GET(url)

#下载图片
def downLoad_HTMLImg(url, imgFile, headers):
    resp1 = HttpUtils.GET(url, headers=headers)
    FileUtils.saveFile_img(imgFile, resp1)
    resp1.close()