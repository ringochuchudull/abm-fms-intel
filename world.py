from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


if __name__ == '__main__':
    
    m1 = Market(num_agents=25,steps=500)
    m1.run()
    print(m1.tradeSequence)
    m1.plotStockTrend()

    data = m1.book

    TEST = NormalProcessAgent(id=-1)
    X, Y = TEST.create_ts(data, series=4)
    print(X, Y)
    print(X.shape, Y.shape)