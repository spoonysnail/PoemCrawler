#!/usr/bin/python
# -*- coding: UTF-8 -*-import urllib2,re
import HTMLParser
from sgmllib import SGMLParser
import sys
reload(sys)

sys.setdefaultencoding('utf8')

class MyParser(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_h1 = False
        self.h1s = []
        self.is_td = False
        self.tds = []
        self.is_patent = False
        self.patentContent = []

    def start_li(self, attrs):
        for k,v in attrs:
            #print k,v
            if str(k).strip() == 'class' and str(v).strip() == 'guwencont2':
               # print 'patent '
                self.is_patent = True
                return

    def end_li(self):
        self.is_patent = False

    def start_h1(self, attrs):
        self.is_h1 = True

    def end_h1(self):
        self.is_h1 = False

    def start_td(self, attrs):
        self.is_td = True

    def end_td(self):
        self.is_td = False

    def handle_data(self, text):
        txt = str(text).strip()
        if self.is_h1 == True:
            if not not txt:
                self.h1s.append(txt)
        if self.is_td == True:
            if not not txt:
                self.tds.append(txt)
        if self.is_patent == True:
            if not not txt:
                self.patentContent.append(txt)


