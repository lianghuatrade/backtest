
class candle(object):
    def __init__(self):
        self.symbol = 0.0
        self.open = 0.0
        self.close = 0.0
        self.high = 0.0
        self.low = 99990.0
        self.share = 0
        self.count = 0
        self.time = 0
        self.date = 0
        
        self.lowTime = 0
        self.highTime = 0
        self.macd = 0.0
        self.macd5k1 = 0.0
        
        self.avg1 = 0.0
        self.avg2 = 0.0
        self.avg3 = 0.0
        self.avg5 = 0.0
        self.avg10 = 0.0
        self.avg20 = 0.0
        self.avg60 = 0.0
        
        self.sizeChange = 0
        
'''
by liuxianwei in hangzhou 233076245
'''
if __name__ == '__main__':
    tK = candle()
    print tK.open
