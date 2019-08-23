
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,sys
import urllib.request 
import time;
import ssl
import logger as L

ssl._create_default_https_context = ssl._create_unverified_context

def flatten(li):
    if True == isinstance(li, tuple):
        li = list(li)
    if False == isinstance(li,list):
        print(li, 'is not `list`');
        return False;

    _list = [];
    for item in li :
        if isinstance(item,list):
            _list.extend(flatten(item))
        else:
            _list.append(item)
    return _list;


def download(remote_path, dir_path):
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
        L.info("saving to: " + file_path)

        urllib.request.urlretrieve(remote_path,file_path,downloading)

        return file_path;
    except IOError as e:
        L.danger("IOError", e)
    except Exception as e:
        L.danger(e, sys._getframe().f_lineno)


