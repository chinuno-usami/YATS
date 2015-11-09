#! /usr/bin/python2
# -*- coding: utf-8-*-
import random
import urllib
import urllib2
import json
import hashlib
import parse_sign

import sys
reload(sys)
sys.setdefaultencoding('gbk')

def send_get(req):
    '''Send get resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor()) 
    for x in xrange(1,4):
        try:
            response = opener.open(req)
            return response.read()
        except Exception, e:
            print 'an error has occurred : %s' % e
    print "network error"
    exit()
    

def post(req,data):  
    '''Send post resquest
    '''
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())  
    for x in xrange(1,4):
        try:
            response = opener.open(req, data) 
            return response.read()
        except Exception, e:
            print 'an error has occurred : %s' % e
    print "network error"
    exit()

# tbs
def gettbs(bduss):
    url_tbs = 'http://tieba.baidu.com/dc/common/tbs'
    req_tbs = urllib2.Request(url_tbs)
    req_tbs_dic = {
                'User-Agent': "fuck phone",
                'X-Forwarded-For': "115.28.1." + str(int(random.random()*253+1)),
                'referer': "http://tieba.baidu.com/",
                "cookie" : "BDUSS="+bduss
                }
    for key in req_tbs_dic:
        req_tbs.add_header(key,req_tbs_dic[key])
    tbs_json = send_get(req_tbs)
    tbs = json.loads(tbs_json)
    if tbs['is_login'] == 1:
        return tbs["tbs"]
    else:
        return False

# list
def getlist(bduss,tbpn):
    url_tblist = 'http://tieba.baidu.com/f/like/mylike?&pn='+str(tbpn)
    req_tblist = urllib2.Request(url_tblist)
    req_tblist_dic = {
                'User-Agent': "Phone XXX",
                "cookie" : "BDUSS="+bduss
                }
    for key in req_tblist_dic:
        req_tblist.add_header(key,req_tblist_dic[key])
    tblist = send_get(req_tblist)
    return  parse_sign.getkw(tblist)

def getlist_all(bduss):
    pn = 1
    url_tblist = 'http://tieba.baidu.com/f/like/mylike?&pn='+str(pn)
    req_tblist = urllib2.Request(url_tblist)
    req_tblist_dic = {
                'User-Agent': "Phone XXX",
                "cookie" : "BDUSS="+bduss
                }
    for key in req_tblist_dic:
        req_tblist.add_header(key,req_tblist_dic[key])
    tblist = send_get(req_tblist)

    tblist_all = []
    pn_last = parse_sign.getpn(tblist)
    while pn <= pn_last:
        tblist_all.extend(getlist(bduss,pn))
        pn = pn + 1
    return tblist_all

#fid 
def getfid(kw):
    url_fid = 'http://tieba.baidu.com/mo/m?kw='+kw
    req_fid = urllib2.Request(url_fid)
    req_fid_dic = {
                'User-Agent': "fuck phone",
                'Referer': 'http://wapp.baidu.com/',
                'Content-Type': 'application/x-www-form-urlencoded'
                }
    for key in req_fid_dic:
        req_fid.add_header(key,req_fid_dic[key])
    fid = send_get(req_fid)
    return parse_sign.getfid(fid)

#sign
def sign(bduss,fid,kw,tbs):
    url_sign = 'http://c.tieba.baidu.com/c/c/forum/sign'
    req_sign = urllib2.Request(url_sign)
    req_sign_dic = {
                'User-Agent': 'Fucking iPhone/1.0 BadApple/99.1',
                'Content-Type': 'application/x-www-form-urlencoded',
                "cookie" : "BDUSS="+bduss
                }
    for key in req_sign_dic:
        req_sign.add_header(key,req_sign_dic[key])

    temp_sign = [
                    ("BDUSS",bduss),
                    ("_client_id",'03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36'),
                    ("_client_type",'4'),
                    ("_client_version",'1.2.1.17'),
                    ("_phone_imei","540b43b59d21b7a4824e1fd31b08e9a6"),
                    ("fid",fid),
                    ("kw",kw),
                    ("net_type",'3'),
                    ("tbs",tbs)
                ]
    sign_sign = ""
    for k,v in temp_sign:
        sign_sign=sign_sign+k+'='+urllib.unquote(v).decode("gbk")

    m_sign = hashlib.md5()
    m_sign.update(sign_sign+'tiebaclient!!!')
    md5_sign = m_sign.hexdigest().upper()
    temp_sign.append(("sign",md5_sign))
    dat_sign = ""
    for k,v in temp_sign:
        dat_sign=dat_sign+k+'='+v+"&"
    dat_sign = dat_sign[:-1]
    rsp_sign = post(req_sign,dat_sign)

    rsp_sign_json = json.loads(rsp_sign)
    if rsp_sign_json["error_code"] == "160002" \
            or rsp_sign_json["error_code"] == "0" \
            or rsp_sign_json["error_code"] == "1101" \
            or rsp_sign_json["error_code"] == "1102":
        return True
    else:
        return False
