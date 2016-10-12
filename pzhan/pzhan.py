#-*- coding:utf-8 -*-

#三方库
import time
from functools import wraps
from utils import HttpUtils, FileUtils, HTMLUtils
#私有库
from mysql.MyDB import Up as UpDB
from utils import ZIPUtils

indexurl = 'http://www.pixiv.net'
memberurlModel = 'http://www.pixiv.net/member.php?id={id}'
bookmarkuserurlModel = 'http://www.pixiv.net/bookmark.php?type=user&id={id}&rest=show&p={page}'
memberillusturlModel = 'http://www.pixiv.net/member_illust.php?id={id}&type=all&p={page}'
bookmarkurlModel = 'http://www.pixiv.net/bookmark.php?id={id}'
mypixivurlModel = 'http://www.pixiv.net/mypixiv_all.php?id={id}'
portraitDir = 'E:\pixiv'
rootdata = '/data'

login_data = {
        'mode': 'login',
        'pass': '159478632',
        'pixiv_id': 'allenlogo',
        'return_to': '/',
        'skip': 1
    }

#登陆
def login():
    if FileUtils.exists(HttpUtils.cookiefile) & FileUtils.isfile(HttpUtils.cookiefile):
        HttpUtils.loadCookies()
    else:
        HttpUtils.POST("https://www.pixiv.net/login.php", postData=login_data)
        HttpUtils.saveCookies()

def getSoup(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            soup = HTMLUtils.get_soup(HttpUtils.GET(args[0]).text)
            result = func(*args, soup=soup, **kwargs)
            return result
    return wrapper

def getError(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as value:
                print("函数：[%s]参数args：[%s]参数kwargs：[%s]异常：[%s]" % (func.__name__, args, kwargs, value))
    return wrapper

#提取用户信息
@getError
@getSoup
def saveUp(url=None, soup=None):
    table = soup.find('table', attrs={'class': "ws_table"})
    saveUp(url.split("id=", 1)[1], table.findAll('tr')[0].findAll('td')[1].text, url)

#保存用户信息
@getError
def saveUp(pid, name, url):
    date = time.strftime('%Y%m%d', time.localtime(time.time()))
    up = UpDB(pid=pid, name=name, url=url, recdate=date)
    up.save()

#提取用户关注
@getError
@getSoup
def getBookMark(bookmarkurl, soup=None):
    userList = soup.find('div', attrs={'class': 'members'}).find('ul')
    for userLi in userList.findAll('li'):
        userA = userLi.find('a', attrs={'class': "ui-profile-popup"})
        print(userA['data-user_id'])
        FileUtils.createdir(FileUtils.joinPath(portraitDir, userA['data-user_id']))
        imgFile = FileUtils.joinPath(portraitDir, userA['data-user_id'], ("%s.%s" % (userA['data-user_id'], userA['data-profile_img'][-3:])))
        HTMLUtils.downLoad_HTMLImg(userA['data-profile_img'], imgFile)
        saveUp(userA['data-user_id'], userA['data-user_name'], "http://www.pixiv.net/%s" % userA['href'])
        scanningMemberillust(userA['data-user_id'], 20)
        ZIPUtils.zip_dir(FileUtils.joinPath(portraitDir, userA['data-user_id']), FileUtils.joinPath(rootdata, "zip", "%s.zip" % userA['data-user_id']))
    return len(userList)

#扫描用户
@getError
def scanningBookMark(pid, lenth):
    print(pid)
    page = 1
    userList = lenth
    while userList == lenth:
        userList = getBookMark(bookmarkuserurlModel.replace("{id}", pid).replace("{page}", str(page)))
        print("已经扫描用户%d" % ((page-1)*lenth+userList))
        page += 1

#扫描用户作品
@getError
def scanningMemberillust(pid, lenth):
    page = 1
    userList = lenth
    while userList == lenth:
        userList = getMemberillust(memberillusturlModel.replace("{id}", pid).replace("{page}", str(page)), pid)
        print("已经扫描用户[%s]作品[%d]" % (pid, (page - 1) * lenth + userList))
        page += 1

#提取作品
@getError
@getSoup
def getMemberillust(memberillusturl, pid, soup=None):
    illusts = soup.find('ul', attrs={'class': '_image-items'})
    i = 0
    for illust in illusts.findAll('li'):
        illustA = illust.find('a')
        checkMemberillust("%s%s" % (indexurl, illustA['href']), pid)
        i = i + 1
    return i

#读取作品图片，标签
@getError
@getSoup
def checkMemberillust(memberillusturl, pid, soup=None):
    #读取标签
    tags = getTags(soup)
    img = soup.find('div', attrs={'class': '_layout-thumbnail ui-modal-trigger'})
    if img:
        FileUtils.createdir(FileUtils.joinPath(portraitDir, pid))
        imgFile = FileUtils.joinPath(portraitDir, pid, ("%s.%s" % (memberillusturl.split('=', 2)[2], img.find('img')['src'][-3:])))
        HTMLUtils.downLoad_HTMLImg(img.find('img')['src'], imgFile)
    else:
        img = soup.find('div', attrs={'class': 'works_display'})
        if img.find('a', attrs={'class': r' _work multiple '}):
            img1 = img.find('a', attrs={'class': r' _work multiple '})
        if img.find('a', attrs={'class': r' _work manga multiple '}):
            img1 = img.find('a', attrs={'class': r' _work manga multiple '})
        checkMemberillust_medium("%s%s%s" % (indexurl, '/', img1['href']), pid, img1['href'].split('=', 2)[2])

#读取画集
@getError
@getSoup
def checkMemberillust_medium(memberillusturl, pid, medium_id, soup=None):
    sections = soup.find('section', attrs={'class': 'manga'})
    for section in sections.findAll('div', attrs={'class': 'item-container'}):
        img = section.find('a', attrs={'class': "full-size-container _ui-tooltip"})
        HTMLData = HttpUtils.GET("%s%s"% (indexurl, img['href']))
        soup = HTMLUtils.get_soup(HTMLData.text)
        img = soup.find('img')
        FileUtils.createdir(FileUtils.joinPath(portraitDir, pid, medium_id))
        imgFile = FileUtils.joinPath(portraitDir, pid, medium_id, FileUtils.getfile(img['src']))
        HTMLUtils.downLoad_HTMLImg(img['src'], imgFile)

def getTags(soup):
    Tags = []
    tags = soup.find('span', attrs={'class': 'tags-container'}).find('ul')
    for tag in tags:
        Tags.append(tag.find('a', attrs={'class': 'text'}).text)
    return Tags

if __name__ == '__main__':
    login()
    scanningMemberillust('14657', 20)
    print('saomiaoguanzhu')
    scanningBookMark('14657', 40)