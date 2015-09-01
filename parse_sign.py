#! /usr/bin/python2
# -*- coding: utf-8-*-
import urllib2
from sgmllib import SGMLParser

# SGMLParser
class tbkw(SGMLParser):
    '''parse tieba kw'''
    def __init__(self):
        SGMLParser.__init__(self)
        self.kw = []
    def start_a(self, attrs):
        self.href = [v[6:] for k,v in attrs if k =='href' and ('/f?kw' in v)]
        if self.href:
            self.kw.extend(self.href)
class tbpn(SGMLParser):
    '''parse tieba list pagenumber'''
    def __init__(self):
        SGMLParser.__init__(self)
        self.is_a = ""
        self.pn = ""
        self.href = ""
    def start_a(self, attrs):
        self.is_a = 1
        self.href = [v for k,v in attrs if k =='href' and ('like?&pn=' in v)]
    def end_a(self):
        self.is_a = ""
    def handle_data(self, text):
        if self.is_a == 1 and self.href:
            self.pn = self.href[-1][19:]

class tbfid(SGMLParser):
    '''parse tieba fid'''
    def __init__(self):
        SGMLParser.__init__(self)
        self.fid = ""
    def start_input(self, attrs):
        for k,v in attrs:
            if v == "fid":
                for k2,v2 in attrs:
                    if k2 == "value":
                        self.fid = v2
                
def getkw(dat):
    '''return a list'''
    tbkwer = tbkw()
    tbkwer.feed(dat)
    return tbkwer.kw
def getpn(dat):
    tbpner = tbpn()
    tbpner.feed(dat)
    pn = tbpner.pn
    if pn:
        return int(tbpner.pn)
    else:
        return 1
def getfid(dat):
    tbfider = tbfid()
    tbfider.feed(dat)
    return tbfider.fid

