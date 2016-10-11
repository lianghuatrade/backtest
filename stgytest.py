from pddata import *
from onestk import *
from plstat import *
import traceback


class context(object):
    start_date=20001001
    end_date=20001001
    cycle=0
    stkmap={}
    result={}
    
    pd=pddata()
    bk=0
    #print index72
    
    def __init__(self):
        pass

def processBanStock(onebarg):
    
    freeze_support()
    test=pddata()
    tmpdata=onebarg.split(',')
    stkmap={}
    stks={}
    if len(tmpdata)==4:
        stks=test.get_bankuai_stocks(tmpdata[0],start_date=int(tmpdata[1]),end_date=int(tmpdata[2]),cycle=int(tmpdata[3]))
    #print len(stks),'----'
    for sym,onestk in stks.iteritems():
        try:
            #print sym,'-----'
            if onestk.close.shape[0] > 1:
                stkk=test.getdeqk(onestk)
                obj=None
                if stkmap.has_key(sym):
                    obj=stkmap[sym]
                else:
                    obj=oneStock(sym,int(tmpdata[3]))
                for k in stkk:
                    obj.add(k,stkk,onestk)
                    #break
                obj.pan.ret().to_csv(sym+'_result.csv')
        except:
            traceback.print_exc() 
            print sym,'---error'
            
def processStock(onebarg):
    
    freeze_support()
    test=pddata()
    tmpdata=onebarg.split(',')
    onestk=None
    if len(tmpdata)==4:
        onestk=test.getdata(tmpdata[0],start_date=int(tmpdata[1]),end_date=int(tmpdata[2]),cycle=int(tmpdata[3]))
    else:
        return
    #print len(stks),'----'
    try:
        #print sym,'-----'
        if onestk.close.shape[0] > 1:
            stkk=test.getdeqk(onestk)
            obj=oneStock(tmpdata[0],int(tmpdata[3]))
            for k in stkk:
                obj.add(k,stkk,onestk)
                #break
            obj.pan.ret().to_csv(tmpdata[0]+'_result.csv')
    except:
        traceback.print_exc() 
        print tmpdata[0],'---error'
                  




if __name__ == '__main__':
##    context.cycle=60
##    context.start_date='20160801'
##    context.end_date='20160801'
  
    
##    pddata.start_date='20160923'
##    pddata.end_date='20160923'
##    pddata.cycle=60
##    context.bk=context.pd.get_bankuailist()
##    print context.bk
        
    #processBanStock(context.bk[0])

    processStock('sz002208,'+'20160823,'+'20160823,300')
    
##    procpl_dayprofit(filename='sh600113_pllog_ordermgr_20161008.csv')
##    procpl_dayprofitlv(filename='sh600113_pllog_ordermgr_20161008.csv')
##



    
##    num_cores=mp.cpu_count()
##    pool=mp.Pool(num_cores)
##    results = pool.map(processStock, context.bk)
##    print results
##    print "--------60---ok----------"

    
##    pddata.cycle=300
##    context.processindex()
##    
##    num_cores=mp.cpu_count()
##    pool=mp.Pool(num_cores)
##    results = pool.map(processStock, context.bk)
##    print results
##    print "--------300---ok----------"
##
