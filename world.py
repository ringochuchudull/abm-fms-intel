from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt

if __name__ == '__main__':
    m1 = Market(num_agents=20)
    for i in range(140):
        m1.trade()


    print(m1.book)
    print(m1.num_buyer,m1.num_seller)
    plt.plot(m1.book)
    plt.show()