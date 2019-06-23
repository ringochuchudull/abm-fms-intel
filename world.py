from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    m1 = Market(num_agents=5,steps=100)
    m1.run()

    print(m1.book)
    print(m1.num_buyer,m1.num_seller)
    m1.plotStockTrend()