from utility import *
from agent import *
from market import *
import random
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')


if __name__ == '__main__':
    
    m1 = Market(num_agents=25,steps=1200)
    m1.run()
    print(m1.tradeSequence)
    m1.plotStockTrend()

    
    '''
    train_data, test_data = data[:492], data[:9]
    TEST = NormalProcessAgent(id=-1)
    X, Y = TEST.create_ts(train_data, series=7)
    T_X, T_Y = TEST.create_ts(test_data, series=7)
    TEST.trainPredictor(X,Y)

    print(len(m1.tradeSequence), len(m1.book) )

    print(X, Y)
    print(X.shape, Y.shape)

    plot_train = TEST.predictPredictor(X)
    plot_test = TEST.predictPredictor(T_X)
    
    p_t = np.concatenate((plot_train, plot_test) , axis=0)

    #print(plot_train.shape, plot_test.shape)

    plt.plot(m1.book)
    plt.plot(p_t)
    #plt.plot(p_t)
    plt.show()
    '''