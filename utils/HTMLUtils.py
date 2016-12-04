# -*- coding:utf-8 -*-

import os
from bs4 import BeautifulSoup
from .import HttpUtils, MyException, FileUtils

@MyException.raiseException
def get_soup(htmldata):
    return BeautifulSoup(htmldata, "html.parser", exclude_encodings="utf-8")

@MyException.raiseException
def get_HTMLPage(url):
    return HttpUtils.GET(url)

@MyException.raiseException
def downLoad_HTMLPage(url, pid):
    HTML_page = HttpUtils.GET(url)
    with open("%s.txt" % pid, "w", encoding="utf-8") as f:
        f.write(HTML_page.text)

@MyException.raiseException
def downLoad_HTMLImg(url):
    return HttpUtils.GET(url)

def downLoad_HTMLImg(url, imgFile, headers):
    try:
        resp1 = HttpUtils.GET(url, Myheaders=headers)
        FileUtils.saveFile_img(imgFile, resp1)
        resp1.close()
    except:
        if FileUtils.exists(imgFile):
           os.remove(imgFile)
        downLoad_HTMLImg(url, imgFile, headers)
        raise