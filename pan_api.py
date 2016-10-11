# -*- coding: cp936 -*-
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
import datetime
import logging,json
import time
from candle import *
#from sklearn import datasets, linear_model

class pan_api(object):
    
    logging.basicConfig(filename='work_trace.log', level=logging.DEBUG)
    outlogging = logging.getLogger("panzheng")
    def __init__(self,symbol,cycle):#
        self.symbol=symbol
        self.cycle=cycle
        
        self.result=pd.DataFrame(np.random.random_sample((240,31))-9999,columns=['symbol','indexbegin','maxup','maxdown','minmaxmaxdiff','maxminmindiff','maxminvibtmpvib','firstkhightmppan','firstklowtmppan','firstkhigh','firstklow','indexend','date','maxminvib','upvib','panvib','updown','newupdown','totalup','upratio','start','end','max1','min1','chuancnt','vib','median1','devia','change','cnt','chuanlv'])
        self.ren=0
        self.reset()

        l=range(240)
        self.ou=[i for i in l if i%2==0]
        self.ji=[i for i in l if i%2!=0]

        
    def reset(self):
        self.pand=pd.DataFrame(np.random.random_sample((240,10))-9999,columns=['date','time','open','lastclose','close','high','low','share','test','mark'])
        self.n=0

        self.pann=0
        self.contcnt=0
        self.panonen=0
        
    def add(self,k):
        if self.n > 1:
##            if k.date != self.pand.iloc[0,:].date:
##                self.reset()
            self.pand.iloc[self.n]=[k.date,k.time,k.open,self.pand.iloc[self.n-1].close,k.close,k.high,k.low,k.share,0,0]
        else:
            self.pand.iloc[self.n]=[k.date,k.time,k.open,k.close,k.close,k.high,k.low,k.share,0,0]
        
        self.n=self.n+1
        if self.n > 1:
            return self.calc_pan()

    def convert_time(self,timesrc):
        tmp=int(timesrc)
        return (tmp/3600)*10000+(tmp%3600/60)*100

    def calc_value(self,pann,tmpcnt):
        tmp=self.pand.iloc[pann:tmpcnt+1,:]#��ӡ������+��ֵ+��׼��+������ǵ���+����+��ĺ��̵ĸ�������+----��Ӱ�ߺ���Ӱ�ߵı���
        tmp.test=(tmp.open+tmp.close)/2
        tmppan=np.mean(tmp.test)
        #tmppandiff=np.mean(tmp.test)
##        nowk=self.pand.iloc[nowcnt,:]
##        #print nowk
##        nowpan=(nowk.open+nowk.close)/2
        
        tmpmax=np.float64(np.max(tmp.high)).item()
        tmpmin=np.float64(np.min(tmp.low)).item()
        #print 'xxxx',type(tmpmax)
        
        

        #panzhenglv
        tmp.test=abs(tmp.open-tmp.close)/tmp.close
        tmppanvib=np.mean(tmp.test)     #tmpmax/tmpmin-1#

        
        #tmpvib111=float(np.float64(tmpvib).item())
        tmpstd=round(np.std(tmp.test),4)#4)
        lastk=self.pand.iloc[tmpcnt,:]
        updown=(lastk.close-self.pand.iloc[pann,:].close)/self.pand.iloc[pann,:].close
        newupdown=(lastk.close-self.pand.iloc[pann-1,:].close)/self.pand.iloc[pann-1,:].close

        tmp.test=tmp.close-tmp.open
        lowcnt=tmp[tmp.test < 0.0].shape[0]
        if lowcnt < 0.001:
            lowcnt = 1
        highcnt=tmp[tmp.test > 0.0].shape[0]
        chuanup=tmp[tmp.high > tmppan   ] #and tmp.low < tmppan
        chuandown=tmp[tmp.low < tmppan   ]
        chuancnt=chuanup.index.intersection(chuandown.index).shape[0]
        
        tpmline=tmp.shape[0]
        upcnt=tmp[tmp.close > tmp.open].shape[0]
        #print '---chuanup=',tpmline,'=chuancnt=',chuancnt
        totalup=np.mean((tmp.close-tmp.lastclose)/tmp.lastclose)

        tmp.test=tmp.high/tmp.low -1
        tmpvib=np.mean(tmp.test)

        minmaxmaxdiff=(tmpmax-np.min(tmp.high))/tmpmax
        maxminmindiff=(np.max(tmp.low) - tmpmin)/tmpmin
        maxup=np.max((tmp.close-tmp.lastclose)/tmp.lastclose)
        maxdown=np.min((tmp.close-tmp.lastclose)/tmp.lastclose)
        
        
        return tmpvib,tmppan,tmpstd,updown,tpmline,highcnt,lowcnt,tmpmax,tmpmin,chuancnt,upcnt,totalup,tmppanvib,newupdown,minmaxmaxdiff,maxminmindiff,maxup,maxdown
    def equals(self,a,b):
        if abs(a-b) < 0.0001:
            return True
        else:
            return False

    def sigmoid(self,X,Max,Min):    
        return (X-Min)*1.0/(Max-Min)

    
    def proc_one_pan(self,pann,tmpcnt):
        retdeq = []
        tmpvib,tmppan,tmpstd,updown,tmpline,highcnt,lowcnt,tmpmax,tmpmin,chuancnt,upcnt,totalup,tmppanvib,newupdown,minmaxmaxdiff,maxminmindiff,maxup,maxdown=self.calc_value(pann,tmpcnt)
            
        tmpfar=tmpmax - tmppan
        tmpfar2=tmppan - tmpmin
        tmphl=tmpmax/tmpmin - 1
        upvi=abs(totalup)/tmpvib
        tmpfirstk=self.pand.iloc[pann,:]
        tmpfirstNextk=self.pand.iloc[pann+1,:]
        tmptailk=self.pand.iloc[tmpcnt,:]
        onexie=(tmpfirstk.close - tmpfirstk.lastclose)/tmpfirstk.lastclose
        nextxie=(tmpfirstk.close - tmpfirstk.open)/tmpfirstk.open
        maxminvib=tmpmax/tmpmin-1#and tmpfirstk.high/tmpfirstk.low-1 < 2*tmpvib
        #print self.pand
        #print 'proc_one_pan----',tmphl,tmpvib,upvi,tmpstd,maxminvib,tmppan,tmpfirstk.high,tmpfirstk.low
        '''
        1��tmphl < 4*tmpvib  maxminvib/tmpvib < 3.5 ----------�����������߼���ͼ۵Ĳ����� С�� 3.5����ƽ��������
        2��upvi < 0.3��upvi----------ÿ��K�ߵ��ǵ������ / ������ < 0.3
        3��tmpstd < 0.0012----------��׼��С��0.0012
        4��tmpfirstk.high > tmppan and tmpfirstk.low < tmppan----------��һ������ߣ���ʹ�Խ��λ��
        5��abs(tmpfirstk.high - tmppan)/tmppan < 3*tmpvib and abs(tmpfirstk.low - tmppan)/tmppan < 3*tmpvib----------��һ���Ĳ����� С�� 3���Ĳ�����
        6��tmpline  ������ܸ��� >= 3
        7������ϲ�����ߺ���ͼ۸��Ǻϲ�
        8.���µͻ��¸ߣ������
        updown=�ǵ�����ƽ��ֵ��������������ǵ���
        newupdown=��������������ǵ���
        '''
        #tmphl/tmpvib < 4 and
        maxminvibtmpvib=maxminvib/tmpvib
        firstkhightmppan=abs(tmpfirstk.high - tmppan)/tmppan/tmpvib
        firstklowtmppan=abs(tmpfirstk.low - tmppan)/tmppan/tmpvib
        bcomb=False

##        tmp=self.pand.iloc[pann:tmpcnt+1,:]
##        tmp.mark=(tmp.close-tmp.lastclose)/tmp.lastclose
##        maxup=tmp.mark.max()
##        maxdown=tmp.mark.min()
##        print tmp
##        print tmp.mark
##        print tmp.mark.max()
        
        #print self.convert_time(self.pand.iloc[pann,:].time),self.convert_time(self.pand.iloc[tmpcnt,:].time),'------',tmptailk.low,tmpmin,upvi,tmppanvib,maxminvib,maxup,maxdown,maxminmindiff,minmaxmaxdiff,maxminvibtmpvib,tmpvib,',upvi=',upvi,tmpstd,maxminvibtmpvib,tmpfirstk.high,tmpfirstk.low,tmppan,firstkhightmppan,firstklowtmppan
        #print '+++++++++++++'
        #print str(tmptailk.low > tmpmin - 0.0001),str(upvi < 0.1),str(tmppanvib < 0.003),str(maxminvib < 0.006),str(maxup < 0.004),str(maxdown > -0.004),str(maxminmindiff < 0.003),str(minmaxmaxdiff < 0.003),str(maxminvibtmpvib < 3),str(tmpvib < 0.002),str(upvi < 0.3),str(tmpstd < 0.0012),str(maxminvibtmpvib < 3.5 ),str(tmpfirstk.high > tmppan),str(tmpfirstk.low < tmppan),str(firstkhightmppan < 3),str(firstklowtmppan < 3)
        if  tmptailk.low > tmpmin - 0.0001 and upvi < 0.1 and tmppanvib < 0.003 and maxminvib < 0.006 and maxup < 0.004 and maxdown > -0.004 and  maxminmindiff < 0.003 and minmaxmaxdiff < 0.003 and maxminvibtmpvib < 3 and tmpvib < 0.003 and tmpstd < 0.0012  and maxminvibtmpvib < 3.5  and firstkhightmppan < 3 and firstklowtmppan < 3:
            tmplv=0.0##and tmpfar < 5*tmpstd and tmpfar2 < 5*tmpstd:  and tmpfirstk.high > tmppan and tmpfirstk.low < tmppan
            tmpuplv=0.0
            #print self.convert_time(self.pand.iloc[pann,:].time),self.convert_time(self.pand.iloc[tmpcnt,:].time),'~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'
            if tmpline > np.int(0):
                    tmplv=chuancnt*1.0/tmpline
                    tmpuplv=upcnt*1.0/tmpline
            if self.result.shape[0] > 0 and self.ren > 0:
                #print self.convert_time(self.pand.iloc[pann,:].time),self.convert_time(self.pand.iloc[tmpcnt,:].time),'^^^^^^^^^^^^~~~~~~~~~~~~~',tmpmax,self.result.iloc[self.ren-1].max1,tmpmin,self.result.iloc[self.ren-1].min1
                if self.equals(tmpmax,self.result.iloc[self.ren-1].max1)    and self.equals(tmpmin,self.result.iloc[self.ren-1].min1):
                    #print self.convert_time(self.pand.iloc[pann,:].time),self.convert_time(self.pand.iloc[tmpcnt,:].time),'^^^^^^^^^^^^~~~~~~~~~~~~~^^^^^^^^^^'
                    if self.result.iloc[self.ren-1].indexbegin < pann:
                        pann = int(self.result.iloc[self.ren-1].indexbegin)
                    self.ren=self.ren-1
                    bcomb=True
                    tmpvib,tmppan,tmpstd,updown,tmpline,highcnt,lowcnt,tmpmax,tmpmin,chuancnt,upcnt,totalup,tmppanvib,newupdown,minmaxmaxdiff,maxminmindiff,maxup,maxdown=self.calc_value(pann,tmpcnt)
                if pann <= self.result.iloc[self.ren-1].indexbegin:
                    #pann=np.int(self.result.iloc[self.ren-1].indexbegin)
                    self.ren=self.ren-1
                    bcomb=True
                    tmpvib,tmppan,tmpstd,updown,tmpline,highcnt,lowcnt,tmpmax,tmpmin,chuancnt,upcnt,totalup,tmppanvib,newupdown,minmaxmaxdiff,maxminmindiff,maxup,maxdown=self.calc_value(pann,tmpcnt)
                    
            #tmp=self.pand.iloc[pann:tmpcnt+1,:]
            #regr = linear_model.LinearRegression()

##            tmplist=[]
##            tmpi=0
##            while tmpi <tmp.shape[0] :
##                tmpret=self.sigmoid(tmpi+1,200,1)
##                tmplist.append([tmpret])
##                tmpi=tmpi+1
##            
##            tmplistY=[]#tmp.close.tolist()
##            tmpi=0
##            tmpdff=0.0
##            while tmpi <tmp.shape[0] :
##                tmplistY.append(self.sigmoid(tmp.iloc[tmpi].close,self.pand.iloc[0].open*1.15,self.pand.iloc[0].open*0.95))
##                tmpi=tmpi+1
##
####            print tmplist
####            print tmplistY            
####            print tmp.close.tolist()
##            #print tmp.close.tolist()#,tmp.close.shape[1],tmp.close
##            regr.fit(tmplist, tmplistY)
##            if pann == 4 and tmpcnt == 6:
##                
##                plt.scatter(tmplist,tmplistY,color='blue')  
##                plt.plot(tmplist,regr.predict(tmplist),color='red',linewidth=4)  
##                plt.xticks(())  
##                plt.yticks(())  
##                plt.show()  
##            if self.n < 20:
##                return
##            tmpallcnt=240
##            if self.cycle > 60:
##                tmpallcnt=48
##            #tmp=self.pand.iloc[2:4+1,:]
##            tmplist=[]
##            tmpi=0
##            while tmpi <tmp.shape[0] :
##                tmpret=self.sigmoid(tmpi+1,tmpallcnt,1)
##                tmplist.append([tmpret])
##                tmpi=tmpi+1
##            
##            tmplistY=[]#tmp.close.tolist()
##            tmpi=0
##            tmpdff=0.0
##            while tmpi <tmp.shape[0] :
##                tmplistY.append(self.sigmoid(tmp.iloc[tmpi].close,self.pand.iloc[0].open*1.1,self.pand.iloc[0].open*0.9))
##                tmpi=tmpi+1
##            regr.fit(tmplist, tmplistY)
            #print '------ok--------',self.result
            #print '---+++---ok-----+++---',self.ren

            tmptailk=self.pand.iloc[tmpcnt,:]        
            tmp=self.pand.iloc[pann:tmpcnt,:]
            tmp1=tmp.open.min()
            tmp2=tmp.close.min()
            tmpmin111 = tmp2 if  tmp1 > tmp2 + 0.0001 else(tmp1)
            tmp1=tmp.open.max()
            tmp2=tmp.close.max()
            tmpmax111 = tmp2 if  tmp1 < tmp2 - 0.0001 else(tmp1)
            if tmptailk.close < tmpmin111 - 0.0001 or tmptailk.close > tmpmax111 + 0.0001:
                if bcomb:
                    self.ren=self.ren+1
                return False
            #print self.convert_time(self.pand.iloc[pann,:].time),self.convert_time(self.pand.iloc[tmpcnt,:].time),'~~~~~~~~~~~~~~~~~~~~~$$$$$$$$$$$$$$$'
            self.result.iloc[self.ren].maxup=maxup#�������������k�ߵ����Ƿ���
            self.result.iloc[self.ren].maxdown=maxdown#����������µ�k�ߵ��µ�����
            self.result.iloc[self.ren].minmaxmaxdiff=minmaxmaxdiff#��������ߵ� -������ÿ��K����ߵ����Сֵ��/������ߵ�
            self.result.iloc[self.ren].maxminmindiff=maxminmindiff #��������ÿ��K����͵�����ֵ-������͵㣩/������͵�
            self.result.iloc[self.ren].firstkhightmppan=firstkhightmppan#����һ����ߵ�-�������λ�ߣ�/������λ��/ƽ��������
            self.result.iloc[self.ren].firstklowtmppan=firstklowtmppan#����һ����͵�-�������λ�ߣ�/������λ��/ƽ��������
            self.result.iloc[self.ren].maxminvibtmpvib=maxminvibtmpvib#regr.coef_#��������߼�/������ͼ�-1��/����ƽ��������
            self.result.iloc[self.ren].symbol=self.symbol
            self.result.iloc[self.ren].indexbegin=pann#��������±�
            self.result.iloc[self.ren].indexend=tmpcnt#���������±�
            self.result.iloc[self.ren].date=self.pand.iloc[self.n-1,:].date#
            self.result.iloc[self.ren].newupdown=newupdown#����
            self.result.iloc[self.ren].firstkhigh=tmpfirstk.high#
            self.result.iloc[self.ren].firstklow=tmpfirstk.low#
            self.result.iloc[self.ren].upvib=upvi#����ÿ��k���ǵ����ľ�ֵ/���䲨����
            self.result.iloc[self.ren].panvib=tmppanvib#����ÿ��K�߿����յĲ����� �ľ�ֵ
            self.result.iloc[self.ren].updown=abs(totalup)/updown#����ÿ��k���ǵ����ľ�ֵ/�������ǵ���
            self.result.iloc[self.ren].totalup=totalup#����ÿ��k���ǵ����ľ�ֵ
            self.result.iloc[self.ren].start=self.convert_time(self.pand.iloc[pann,:].time)#������ʼʱ��
            self.result.iloc[self.ren].end=self.convert_time(self.pand.iloc[tmpcnt,:].time)#��������ʱ��
            self.result.iloc[self.ren].max1=tmpmax#������������ֵ
            self.result.iloc[self.ren].min1=tmpmin#�����������Сֵ
            self.result.iloc[self.ren].upratio=tmpuplv#����k�߸���/��K�߸���
            self.result.iloc[self.ren].chuancnt=chuancnt
            self.result.iloc[self.ren].vib=tmpvib#��������Ĳ�����
            self.result.iloc[self.ren].median1=tmppan#�����������λ��
            self.result.iloc[self.ren].devia=tmpstd#��������ı�׼��
            self.result.iloc[self.ren].change=updown#����������ǵ���
            self.result.iloc[self.ren].maxminvib=maxminvib#������߼�/������ͼ�-1
            

            self.result.iloc[self.ren].cnt=tmpline#��������k�߸���
            
                #print '11111:',chuancnt,tmpline
            self.result.iloc[self.ren].chuanlv=tmplv#������λ�ߵ�K�߸���/�����ܸ���
            self.ren=self.ren+1
                        
            return True
        else:
            return False
        return False
    def calc_pan(self):
        tmpcnt=self.n-1
        pann=0
        if tmpcnt > 21:
            pann=tmpcnt - 23
        while pann < tmpcnt - 1:
            if self.proc_one_pan(pann,tmpcnt):         
                return True
            pann = pann+1
        return False
##        pann=tmpcnt -2
##        tmplow=0
##        if tmpcnt > 11:
##            tmplow=tmpcnt - 10
##        while pann > tmplow:
##            if self.proc_one_pan(pann,tmpcnt):         
##                break
##            pann = pann-1
        

    def retDian(self):
##        self.result=self.result.iloc[0:self.ren,]
##        tmp1=pd.DataFrame(np.random.random_sample((2040,2))-9999,columns=['time','side'])
##        tmp1.time=self.result.start
##        tmp1.side=1
##        #tmp1.index=tmp1.time
##
##        tmp2=pd.DataFrame(np.random.random_sample((2040,2))-9999,columns=['time','side'])
##        tmp2.time=self.result.end
##        tmp2.side=2
##        #tmp2.index=tmp2.time
##
##        ret=pd.concat([tmp1,tmp2])
##        ret.index=range(ret.shape[0])
##        #print '-------',self.symbol
##        ret['symbol']=str(self.symbol)
##        print type(ret.symbol.iloc[0])
        return ret[ret.time > 0]
               
    def ret(self,oneret=0):
        if oneret == 1:
            return self.result.iloc[self.ren-1,]
        else:
            return self.result.iloc[0:self.ren,]
        
        #self.result=self.result.iloc[0:self.ren,]
        
        #self.result=self.result[self.result.upratio < 0.83]
##        self.result=self.result[self.result.cnt > 2]
##        #self.result=self.result[self.result.fit3 > 2]
##        #self.result=self.result[self.result.fit6 > 0.35]
##        #plt.plot(x,z,"b--",label="xx")
##        #self.result=self.result[self.result.fit5 > 2]
##        #print self.result
##        tmp1=int(self.result.iloc[0].indexbegin)
##        #print tmp1
##        tmp2=int(self.result.iloc[0].indexend)
##        #print tmp2
##        #print self.pand.iloc[tmp1:tmp2+1,:]

##        nowtmptmp=tmp
##        nowtmptmp.test=nowtmptmp.high/nowtmptmp.low -1
##        #print nowtmptmp,'--------------------------'
##        if nowtmptmp.test.max() > tmpvib*2:            
##            nowtmptmp111=nowtmptmp[nowtmptmp.test != nowtmptmp.test.max()]
##            tmpvib=np.mean(nowtmptmp111.test)     #tmpmax/tmpmin-1#
        
        return self.result.iloc[0:self.ren,]
    

def test():#100stock,1min,3tick   100*60*3=18000
    data=panzheng('')
    k=candle()
    k.time=34200
    k.open=11
    k.close=12
    k.high=15
    k.low=11.5
    data.add(k)
    k.time=34260
    data.add(k)
##    data.add(k)
##    data.add(k)
    #print data.pand
    
##    tmpret=tmp.pand.close.describe()
##    print tmpret.iloc[6] - tmpret.iloc[4]
    
##    test=[]
##    i=0
##    while(i<3000):
##        i=i+1
##        test.append(panzheng(''))
##        #time.sleep(0.1)
##    while(1):
##        time.sleep(0.1)
        

if __name__ == '__main__':
    
    versionV1010="init"
    #test()
##    regr = linear_model.LinearRegression()
##    tmplist=[[5],[8],[]]
##    plt.scatter(tmplist,tmplistY,color='blue')  
##    plt.plot(tmplist,regr.predict(tmplist),color='red',linewidth=4)  
##    plt.xticks(())  
##    plt.yticks(())  
##    plt.show()  
    
