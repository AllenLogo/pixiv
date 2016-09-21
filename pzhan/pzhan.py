#-*- coding:utf-8 -*-

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

indexurl = 'http://www.pixiv.net'
memberurlModel = 'http://www.pixiv.net/member.php?id={id}'
bookmarkuserurlModel = 'http://www.pixiv.net/bookmark.php?type=user&id={id}&rest=show&p={page}'
memberillusturlModel = 'http://www.pixiv.net/member_illust.php?id={id}&type=all&p={page}'
bookmarkurlModel = 'http://www.pixiv.net/bookmark.php?id={id}'
portraitDir = 'D:\pixiv'

#登陆
def login():
    if FileUtils.exists(HttpUtils.cookiefile) & FileUtils.isfile(HttpUtils.cookiefile):
        HttpUtils.loadCookies()
    else:
        HttpUtils.POST("https://www.pixiv.net/login.php", postData=login_data)
        HttpUtils.saveCookies()

#下载页面
def downLoad_HTMLPage(url, pid):
    try:
        HTML_page = HttpUtils.GET(url)
        with open("%s.txt" % pid, "w", encoding="utf-8") as f:
            f.write(HTML_page.text)
    except Exception as value:
        print(value)

#下载图片
def downLoad_HTMLImg(url, imgFile):
    try:
        resp1 = HttpUtils.GET(url)
        FileUtils.saveFile_img(imgFile, resp1)
        resp1.close()
    except Exception as value:
        print("%s_%s" % ("downLoad_HTMLImg", value))

#提取用户信息
def saveUp(url):
    soup = HttpUtils.get_soup(HttpUtils.GET(url))
    table = soup.find('table', attrs={'class': "ws_table"})
    try:
        saveUp(url.split("id=", 1)[1], table.findAll('tr')[0].findAll('td')[1].text, url)
    except Exception as value:
        print(value)

#保存用户信息
def saveUp(pid, name, url):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    try:
        up = UpDB(pid=pid, name=name, url=url, recdate=date)
        up.save()
    except Exception as value:
        print(value)

#提取用户关注
def getBookMark(bookmarkurl):
    HTMLData = HttpUtils.GET(bookmarkurl)
    soup = HttpUtils.get_soup(HTMLData.text)
    userList = soup.find('div', attrs={'class': 'members'}).find('ul')
    for userLi in userList.findAll('li'):
        userA = userLi.find('a', attrs={'class': "ui-profile-popup"})

        FileUtils.createdir(FileUtils.joinPath(portraitDir, userA['data-user_id']))
        imgFile = FileUtils.joinPath(portraitDir, userA['data-user_id'], ("%s.%s" % (userA['data-user_id'], userA['data-profile_img'][-3:])))
        downLoad_HTMLImg(userA['data-profile_img'], imgFile)
        saveUp(userA['data-user_id'], userA['data-user_name'], "http://www.pixiv.net/%s" % userA['href'])
    return len(userList)

#扫描用户
def scanningBookMark(pid, lenth):
    page = 1
    userList = lenth
    while userList == lenth:
        userList = getBookMark(bookmarkuserurlModel.replace("{id}", pid).replace("{page}", str(page)))
        print("已经扫描用户%d" % ((page-1)*lenth+userList))
        page += 1

#扫描用户作品
def scanningMemberillust(pid, lenth):
    page = 1
    userList = lenth
    while userList == lenth:
        userList = getMemberillust(memberillusturlModel.replace("{id}", pid).replace("{page}", str(page)), pid)
        print("已经扫描作品%d" % ((page - 1) * lenth + userList))
        page += 1

#提取作品
def getMemberillust(memberillusturl, pid):
    HTMLData = HttpUtils.GET(memberillusturl)
    soup = HttpUtils.get_soup(HTMLData.text)
    illusts = soup.find('ul', attrs={'class': '_image-items'})
    for illust in illusts.findAll('li'):
        illustA = illust.find('a')
        checkMemberillust("%s%s" % (indexurl, illustA['href']), pid)
    return len(illusts)

#读取作品图片，标签
def checkMemberillust(memberillusturl, pid):
    HTMLData = HttpUtils.GET(memberillusturl)
    soup = HttpUtils.get_soup(HTMLData.text)
    try:
        #读取标签
        tags = getTags(soup)
        img = soup.find('div', attrs={'class': '_layout-thumbnail ui-modal-trigger'})
        if img:
            FileUtils.createdir(FileUtils.joinPath(portraitDir, pid))
            imgFile = FileUtils.joinPath(portraitDir, pid, ("%s.%s" % (memberillusturl.split('=', 2)[2], img.find('img')['src'][-3:])))
            downLoad_HTMLImg(img.find('img')['src'], imgFile)
        else:
            img = soup.find('div', attrs={'class': 'works_display'}).find('a', attrs={'class': ' _work multiple '})
            checkMemberillust_medium("%s%s%s" % (indexurl, '/', img['href']), pid, img['href'].split('=', 2)[2])
    except Exception as value:
        print(memberillusturl)
        print(value)

#读取画集
def checkMemberillust_medium(memberillusturl, pid, medium_id):
    HTMLData = HttpUtils.GET(memberillusturl)
    soup = HttpUtils.get_soup(HTMLData.text)
    sections = soup.find('section', attrs={'class': 'manga'})
    for section in sections.findAll('div', attrs={'class': 'item-container'}):
        img = section.find('a', attrs={'class': "full-size-container _ui-tooltip"})
        HTMLData = HttpUtils.GET("%s%s"% (indexurl, img['href']))
        soup = HttpUtils.get_soup(HTMLData.text)
        img = soup.find('img')
        FileUtils.createdir(FileUtils.joinPath(portraitDir, pid, medium_id))
        imgFile = FileUtils.joinPath(portraitDir, pid, medium_id, FileUtils.getfile(img['src']))
        downLoad_HTMLImg(img['src'], imgFile)

def getTags(soup):
    Tags = []
    tags = soup.find('span', attrs={'class': 'tags-container'}).find('ul')
    for tag in tags:
        Tags.append(tag.find('a', attrs={'class': 'text'}).text)
    return Tags

if __name__ == '__main__':
    login()
    scanningMemberillust('6815602', 20)