from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    m1 = Market(num_agents=30,steps=150)
    m1.run()
    m1.plotStockTrend()

    #print(m1.book)
    #print(m1.num_buyer,m1.num_seller)
    #m1.plotStockTrend()
    #import numpy as np
    #import matplotlib.pyplot as plt

    #plt.axis([0, 10, 0, 1])
    #for i in range(10):
    #   y = np.random.random()
    #    plt.scatter(i, y)
    #    plt.pause(0.1)
    #plt.show()