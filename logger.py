
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,time;
from utils import flatten;


class Logger:
    file_path = ''
    file_handler = None
    def __init__(self, file_dir =  os.getcwd()):
        file_dir = file_dir + '/logs';
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        self.file_path = file_dir + '/porn.log-' + time.strftime("%Y-%m-%d", time.localtime());
        self.file_handler = open(self.file_path, 'a+');
    def print(self, *content):
        datetime = time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime());
        self.file_handler.writelines(flatten([datetime,list(content), "\n"]));
    def info(self, *content):
        self.print("[info]", *content)
    def warning(self, *content):
        self.print("[warning]", *content)
    def danger(self, *content):
        self.print("[danger]", *content)
    def __del__(self):
        self.file_handler.close()

l = Logger()
def info(*content): 
    l.info(*content)
def warning(*content): 
    l.info(*content)
def danger(*content): 
    l.info(*content)