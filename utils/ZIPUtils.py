# -*- coding:utf-8 -*-
import os
import zipfile

def zip_dir(dirname, zipfilename):
    """
    | ##@函数目的: 压缩指定目录为zip文件
    | ##@参数说明：dirname为指定的目录，zipfilename为压缩后的zip文件路径
    | ##@返回值：无
    | ##@函数逻辑：
    """
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
 
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

if __name__ == '__main__':
    import sys
    zip_dir(sys.argv[1], sys.argv[2])
