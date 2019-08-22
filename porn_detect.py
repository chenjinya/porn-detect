
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,stat
import urllib.request 
import sys,PIL.Image as Image
import string
import numpy
import time;

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

current_path = os.getcwd();

log_path = current_path + '/porn.log-' + time.strftime("%Y-%m-%d", time.localtime());
log_file_cache = open(log_path, 'a+');

def flattenList(l):
    if False == isinstance(l,list):
        print(l, 'is not `list`');
        return False;

    _list = [];
    for item in l :
        if isinstance(item,list):
            _list.extend(flattenList(item))
        else:
            _list.append(item)
    return _list;

def log(*content):
    print(content)
    datetime = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime());
    log_file_cache.writelines(flattenList([datetime,list(content), "\n"]));



def downloadFile(remote_path, dir_path):
    def downloading(a,b,c):
        per=100.0*a*b/c
        if per>100:
            per=100
            print('%.2f%%' % per)
        else :
            print('=', end = '' )

    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        arr = os.path.split(remote_path);
        file_name = arr[1];

        file_path = '{}{}{}'.format(dir_path,os.sep,file_name)
        log("saving to: " + file_path)

        urllib.request.urlretrieve(remote_path,file_path,downloading)

        return file_path;
    except IOError as e:
        log("IOError", e)
    except Exception as e:
        log(e, sys._getframe().f_lineno)

def pornDetect(image_path):
    img = Image.open(image_path).convert('YCbCr')
    w, h = img.size
    data = img.getdata()
    cnt = 0
    for i, ycbcr in enumerate(data):
        y, cb, cr = ycbcr
        if 86 <= cb <= 117 and 140 <= cr <= 168:
            cnt += 1
    rate = cnt / ((w * h * 0.16))

    return rate


params1 = sys.argv[1];
log("argv: ", sys.argv)

current_path = os.getcwd();
log("current path: %s"%(current_path))


dir_path='%s/porn_detect_temp'%(current_path)

file_path = downloadFile(params1, dir_path)

log("download file path: %s"%(file_path))

score = pornDetect(file_path)

log_file_cache.close();
os.remove(file_path);
print("porn detect: %s %s %s"%(params1,'socre: ' + str('%.2f' % score),  ' is true' if score > 1 else 'is false'))

