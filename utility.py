import numpy as np

BUY  = 0
SELL = 1
maxP = 2000
minP = 1
draft_param = 0.3

def initbidprice():
    low = maxP/3
    high = maxP/2
    return round(np.random.uniform(low=low, high=high, size=None), 2)

def initsellprice():
    low = maxP/2
    high = maxP*2/3
    return round(np.random.uniform(low=low, high=high, size=None), 2)

def updateSellorBidPrice():
    dd = (1+draft_param)/2
    
    d = np.random.uniform(low=0.0, high=1.0)

    if d < dd: # Approach to dP
        return True
    else: # Step awat from dp
        return False

def buyorsell():
    a = np.random.uniform(low=0.0, high=1.0)
    if a < 0.5:
        return True
    else:
        return False
    
if __name__ == '__main__':
    print(initbidprice())
    print(initsellprice())