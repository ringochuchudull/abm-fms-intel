from utility import *
from agent import *
import random
import matplotlib.pyplot as plt

class Market():
    def __init__(self, num_agents):

        self.num_agents = num_agents
        self.shares = int(num_agents/2)
        
        self.stockprice = int(maxP/1.65)
        self.book = [self.stockprice]

        self.agentlist = []

        self.num_seller = 0
        self.num_buyer = self.num_agents

        self.populate(num_agents)

    def populate(self, n):
        # Create N agents
        for i in range(n):
            self.agentlist.append(ZeroIntelligentAgent(id=i+1, sellprice=initsellprice(), bidprice=initbidprice()))
            self.buyerlist = self.agentlist

    def record_order(self, tranction_price):
        self.book.append(tranction_price)
        self.stockprice = tranction_price

    def trade(self):
        
        try:
            curr_agent = self.agentlist[random.randint(0,self.num_agents-1)]
        except IndexError as e:
            exit()

        # If the agent has one share, this agent is the seller
        if curr_agent.share: 
            curr_agent.sell(market=self)

        # If the agent has no share... 
        else:
            curr_agent.buy(market=self)          

        self.showMarketAgent()

    def showMarketAgent(self):
        print('----------------------')
        for a in self.agentlist:
            print(a)
        print('Current Stock Price £' + str(self.book[-1]) + ' Existing market shares ' +str(self.shares))
        print('----------------------')


# Test 
def _test():
    m1 = Market(num_agents=20)
    for i in range(200):
        m1.trade()

    print(m1.book)
    plt.plot(m1.book)
    plt.show()


if __name__ == '__main__':
    _test()
