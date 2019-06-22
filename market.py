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
            #Return buyer, transaction price
            curr_buyer, transaction_price = curr_agent.sell(market=self)

            if curr_buyer is None:
                self.record_order(self.stockprice)
                print('Cannot find suitable buyer... so Hold')
            
            else:
                self.num_seller -= 1
                self.num_buyer += 1
                self.record_order(transaction_price)
                
                curr_buyer.act(transaction_price)
                self.num_buyer -= 1
                self.num_seller += 1

                print('Agent ' + str(curr_buyer.id) + ' offers to buy the highest price £' + str(transaction_price))
                print('Agent ' + str(curr_agent.id) + ' sell to Agent ' + str(curr_buyer.id) + ' at price £' + str(transaction_price))
            
        # If the agent has no share... 
        else:
            curr_seller, transaction_price = curr_agent.buy(market=self)          

            if curr_seller is None:
                self.record_order(self.stockprice)
                self.shares -= 1
                self.num_buyer -= 1
                self.num_seller += 1
                print('Agent ' + str(curr_agent.id) + ' buys from Market')
            
            else:
                self.record_order(transaction_price)
                self.num_buyer -= 1
                self.num_seller += 1

                curr_seller.act(transaction_price)
                self.num_seller -= 1
                self.num_buyer += 1

                print('Agent ' + str(curr_agent.id) + ' buys from Agent ' + str(curr_seller.id) + ' at price £' + str(transaction_price))
                

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
