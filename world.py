from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    
    m1 = Market(num_agents=20,steps=400)
    m1.run()
    m1.plotStockTrend()
