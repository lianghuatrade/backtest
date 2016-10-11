# -*- coding: cp936 -*-
import numpy as np
import pandas as pd

def procpl_dayprofit(filename='pllog_ordermgr_c0301_20160810.csv'):
    pl=pd.read_csv(filename)
    #print pl
    dst=pd.DataFrame(np.random.randn(1,6),columns=['stgyname','tradedate','profitloss','tradecnt','tradestockcnt','volume'])
    #print dst
    dstcsv=dst
    for date, oneday in pl.groupby('outtime'):
        #print oneday.stgyname
        dst['stgyname']=oneday.iloc[0,0]#pl.iloc[0,0]
    ##    tmp=oneday.symbol.value_counts()
    ##    print tmp.shape[0]
        dst['tradedate']=date
        dst['profitloss']=oneday.profit.sum()
        dst['tradecnt']=oneday.shape[0]
        dst['tradestockcnt']=oneday.symbol.value_counts().shape[0]
        dst['volume']=oneday.lastpos.sum()

        #dst.to_csv('pllog_ordermgr_c0301_20160810_profit.csv')
        #print dst
        dstcsv=pd.concat([dstcsv,dst])
        #dstcsv.append(dst.iloc[0])
    print dstcsv
    dstcsv.to_csv('profit_'+filename)


def  procpl_dayprofitlv(filename='pllog_ordermgr_c0301_20160810.csv'):
    pl=pd.read_csv(filename)
    #print pl
    dst=pd.DataFrame(np.random.randn(1,11),columns=['stgyname','totalcnt','profit','profitcntlv','loss','profitcnt','losscnt','profitlosslv','profitevery','lossevery','profitcntlv'])
    #print dst
    dstcsv=dst

    dstcsv['stgyname']=pl.iloc[0,0]
    dstcsv['totalcnt']=pl.shape[0]
    #dstcsv['profitlv']=0
    #print pl[pl.profit>0.01]
    dstcsv['profit']=pl[pl.profit>0.01].profit.sum()
    dstcsv['loss']=pl[pl.profit<-0.01].profit.sum()
    dstcsv['profitcnt']=pl[pl.profit>0.01].shape[0]
    dstcsv['losscnt']=pl[pl.profit<-0.01].shape[0]
    dstcsv['profitlosslv']=dstcsv['profitcnt']*1.0/dstcsv['losscnt']
    dstcsv['profitevery']=dstcsv['profit']/dstcsv['profitcnt']
    dstcsv['lossevery']=dstcsv['loss']/dstcsv['losscnt']
    dstcsv['profitcntlv']=dstcsv['profitcnt']*1.0/(dstcsv['profitcnt']+dstcsv['losscnt'])
    
    print dstcsv
    dstcsv.to_csv('profit_'+filename)

#procpl_dayprofitlv()
