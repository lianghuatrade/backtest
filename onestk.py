from pan_api import *
from stkordermgr import *


class oneStock(object):
    start_date=20160817
    end_date=20160822
    result={}
    
    def __init__(self,symbol,cycle_raw):
        self.pan=pan_api(symbol,cycle_raw)
        self.symbol=symbol
        self.stkordermgr=stkordermgr(self.symbol)


        
    def add(self,k,allk,df):
        #print "test111"
        #print k.date
        self.stkordermgr.add(k)
        
        ret=self.pan.add(k)
        if ret:
            self.stkordermgr.addenter(k)
        
        return 1
    
##class onestk(object):
##    result={}
##    def __init__(self):
##        pass
##    def add(self,k,allk,df):
##        print "test111"
##        return 1
