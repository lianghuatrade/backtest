# -*- coding: utf-8 -*-
import collections
import os
import copy,traceback
import sys,time,json,datetime
import logging
import logging.config
from candle import *

#NOT_FIND_ORDER=""
NOT_FIND_ORDER=None


class stkordermgr(object):
    
    def __init__(self,symbol,stgyall='tst',feelv=0.0003):
        self.stgy=stgyall
        self.symbol=symbol
        self.feelv=feelv
        
        testdate=datetime.datetime.now().strftime('%Y%m%d')
        self.plogfile=open(self.symbol+"_pllog_ordermgr_"+testdate+".csv","a+")
        self.plogfile.write("stgyname,symbol,owner,lastdate,quotedate,openexepx,opentime,outexepx,outtime,dealmaxpx,dealmaxtime,dealminpx,dealmintime,maxpl,minpl,profit,isnetpl,lastpos,feelv,hs300up,longorshort\n")
        #self.enterlogfile.write("stgyname,symbol,owner,lastdate,quotedate,enterPx,enterTime,lasttime,position,posshizhi,feelv,\n")

        print "ordermgr init done ..."
        self.deq=[]
        self.pos=0
##        self.entermap={}
##        self.enterPosmap={}
##        self.enterMaxmap={}
        self.enterk=None
        self.loss=-0.007
        self.openMaxk=candle()
        
    def convert_time(self,timesrc):
        tmp=int(timesrc)
        ret=(tmp/3600)*10000+(tmp%3600/60)*100
        if ret < 100000:
            return '0'+str(ret)
        return str(ret)
    def addenter(self,k):
        self.pos=100
        self.enterk=k
##        self.entermap[symbol]=k
##        self.enterPosmap[symbol]=100
##        self.enterMaxmap[symbol]=candle()
    def add(self,k):
        if self.pos > 0:
            if self.openMaxk.high < k.high - 0.001:
                self.openMaxk = k
            if (k.close - self.openMaxk.high)/self.openMaxk.high < self.loss:
                outpx=k.close
                profit=self.pos*(outpx-self.enterk.close)-self.pos*(outpx+self.enterk.close)*self.feelv-self.pos*outpx*0.001
                if self.symbol[1] == 'h':
                    profit=profit-self.pos*0.0012
                
                str_out_info=self.stgy+","+self.symbol+",test,"+str(k.date)+","+str(k.date)
                str_out_info=str_out_info+","+str(self.enterk.close)+","+str(k.date)+":"+str(self.convert_time(self.enterk.time))
                str_out_info=str_out_info+","+str(outpx)+","+str(k.date)+":"+str(self.convert_time(k.time))
                str_out_info=str_out_info+","+str(self.openMaxk.high)
                str_out_info=str_out_info+","+str(self.openMaxk.time)
                str_out_info=str_out_info+","+str(0.0)
                str_out_info=str_out_info+","+str(34200)
                str_out_info=str_out_info+","+str(0.0)
                str_out_info=str_out_info+","+str(0.0)
                str_out_info=str_out_info+","+str(profit)
                str_out_info=str_out_info+","+str(1)
                str_out_info=str_out_info+","+str(self.pos)
                str_out_info=str_out_info+","+str(self.feelv)
                str_out_info=str_out_info+","+str(0.0)
                str_out_info=str_out_info+","+str(1)
                self.plogfile.write(str_out_info+"\n")
                self.plogfile.flush()
                self.pos=0
                
##        if self.enterPosmap.has_key(symbol):
##            pos=self.enterPosmap[symbol]
##        if pos > 0:
##            openMaxk=self.enterMaxmap[symbol]
##            enterk=self.entermap[symbol]
##            if openMaxk.high < k.high - 0.001:
##                openMaxk = k
##                self.enterMaxmap[symbol]=openMaxk
##            if (k.low - openMaxk.high)/openMaxk.high < self.loss:
##                outpx=openMaxk.high*self.loss+openMaxk.high
##                profit=self.pos*(outpx-enterk.close)-self.pos*(outpx+enterk.close)*self.feelv-self.pos*outpx*0.001
##                if symbol[1] == 'h':
##                    profit=profit-self.pos*0.0012
##                
##                str_out_info=self.stgy+","+symbol+",test,"+str(k.date)+","+str(k.date)
##                str_out_info=str_out_info+","+str(enterk.close)+",20161010:"+str(enterk.time)
##                str_out_info=str_out_info+","+str(outpx)+",20161010:"+str(k.time)
##                str_out_info=str_out_info+","+str(openMaxk.high)
##                str_out_info=str_out_info+","+str(openMaxk.time)
##                str_out_info=str_out_info+","+str(0.0)
##                str_out_info=str_out_info+","+str(34200)
##                str_out_info=str_out_info+","+str(0.0)
##                str_out_info=str_out_info+","+str(0.0)
##                str_out_info=str_out_info+","+str(0.01)
##                str_out_info=str_out_info+","+str(self.pos)
##                str_out_info=str_out_info+","+str(self.feelv)
##                str_out_info=str_out_info+","+str(0.0)
##                str_out_info=str_out_info+","+str(1)
##                self.plogfile.write(str_out_info+"\n")
##                self.plogfile.flush()
##                #self.pos=0
##                self.enterPosmap[symbol]=0
####        elif self.pos < 0:
####            pass
##


if __name__ == '__main__':
    versionV1016=""
    import ConfigParser
    configFl = ConfigParser.RawConfigParser()
    #configFl.read('quotetools.ini')
    ordermgrtmp=ordermgr("", "", "", 0)
    
