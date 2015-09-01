#! /usr/bin/python2
# -*- coding: utf-8-*-
import parse_sign ,sign_fun
import urllib
import time
import os

def main():
    if not os.path.exists('bduss'):
        print "bduss not found!"
        exit()
    print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),':'
    bduss_list = []
    with open("bduss") as f_bduss :
        for bduss in f_bduss.readlines():
            bduss_list.append(bduss[:-1])
    for bduss in bduss_list:
        if sign_fun.gettbs(bduss) == False:
            print "invalid BDUSS:",bduss
            continue
        tiebalist = sign_fun.getlist_all(bduss)
        for x in xrange(0,3):
            if tiebalist:
                done_list = []
                for tieba in tiebalist:
                    tbs = sign_fun.gettbs(bduss)
                    fid = sign_fun.getfid(tieba)
                    if sign_fun.sign(bduss,fid,tieba,tbs):
                        print urllib.unquote(tieba),"done"
                        done_list.append(tieba)
                    else:
                        print urllib.unquote(tieba),"failed"
                for tb in done_list:
                    tiebalist.remove(tb)
    print "all sign done"
    print "failed list:",tiebalist
if __name__ == '__main__':
    main()