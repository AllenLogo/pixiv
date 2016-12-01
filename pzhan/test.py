#
# import urllib.request
# import os
#
# def Schedule(a,b,c):
#     '''''
#     a:已经下载的数据块
#     b:数据块的大小
#     c:远程文件的大小
#    '''
#     per = 100.0 * a * b / c
#     if per > 100 :
#         per = 100
#     print('%.2f%%' % per)
#
# url = 'http://i1.pixiv.net/img-original/img/2014/04/13/05/21/19/42861912_p0.jpg'
# #local = url.split('/')[-1]
# local = os.path.join('/data/', '59256176_p0.jpg')
# urllib.request.urlretrieve(url, local, Schedule)
import os
from PIL import Image

def getFileList(p):
    p = str(p)
    if p == "":
        return []
    a = os.listdir(p)
    b = [x for x in a if os.path.isfile(p + x)]
    return b


fileList = getFileList("C:\\data\\\pixiv\\")
# for fs in fileList:
#     try:
#         f = open("C:\\data\\\pixiv\\"+fs, "rb")
#         im = Image.open(f)
#         f.close()
#         x, y = im.size
#     except:
#         f.close()
#         os.remove("C:\\data\\\pixiv\\"+fs)

# im = Image.open("C:\\data\\\pixiv\\57081668.jpg")
# print(im.size)

f = open("C:\\data\\\pixiv\\64180.jpg", "ab")

print(os.path.getsize("C:\\data\\\pixiv\\64180.jpg"))

im = Image.open("C:\\data\\\pixiv\\64180.jpg")
x, y=im.size
print(x*y)