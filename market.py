from utility import *
from agent import *
import random
import matplotlib.pyplot as plt

'''

'''
class Market():
    def __init__(self, num_agents, steps):

        self.num_agents = num_agents
        self.shares = int(num_agents/2)
        
        self.stockprice = int(maxP/1.65)
        self.book = []

        self.agentlist = []

        self.num_seller = 0
        self.num_buyer = self.num_agents

        self.populate(num_agents)
        self.steps = steps

    def populate(self, n):
        # Create N agents
        for i in range(n):
            self.agentlist.append(ZeroIntelligentAgent(id=i+1, sellprice=initsellprice(), bidprice=initbidprice()))
            self.buyerlist = self.agentlist

    def record_order(self, tranction_price):
        self.book.append(tranction_price)
        self.stockprice = tranction_price

    def newtrade(self):
        
        curr_agent = self.agentlist[random.randint(0,self.num_agents-1)]
        dealer, transaction_price, direction = curr_agent.newact(market=self)

        if direction is SELL:

            if dealer is None:
                self.record_order(self.stockprice)
                print('Cannot find suitable buyer... so Hold')
            else:
                self.num_seller -= 1
                self.num_buyer += 1
                self.record_order(transaction_price)

                dealer.record(BUY, transaction_price)
                self.num_buyer -= 1
                self.num_seller += 1

                print('Agent ' + str(dealer.id) + ' offers to buy the highest price £' + str(transaction_price))
                print('Agent ' + str(curr_agent.id) + ' sell to Agent ' + str(dealer.id) + ' at price £' + str(transaction_price))
                      
        elif direction is BUY:

                if dealer is None:
                    self.record_order(self.stockprice)
                    self.shares -= 1

                    self.num_buyer -= 1
                    self.num_seller += 1
                    print('Agent ' + str(curr_agent.id) + ' buys from Market')
                
                else:
                    self.record_order(transaction_price)
                    self.num_buyer -= 1
                    self.num_seller += 1

                    dealer.record(SELL, transaction_price)
                    self.num_seller -= 1
                    self.num_buyer += 1

                    print('Agent ' + str(curr_agent.id) + ' buys from Agent ' + str(dealer.id) + ' at price £' + str(transaction_price))
            
        else:
            raise Exception('Neithher Buy nor Sell')

        self.showMarketAgent()

    def run(self):
        for _ in range(self.steps):
            self.newtrade()

    def showMarketAgent(self):
        print('----------------------')
        for a in self.agentlist:
            print(a)
        print('Current Stock Price £' + str(self.book[-1]) + ' Existing market shares ' +str(self.shares))
        print('----------------------')

    def plotStockTrend(self):
        plt.plot(self.book)
        plt.show()

# Test 
def _test():
    m1 = Market(num_agents=30)
    for i in range(400):
        m1.trade()

    print(m1.book)
    m1.plotStockTrend()


if __name__ == '__main__':
    _test()
