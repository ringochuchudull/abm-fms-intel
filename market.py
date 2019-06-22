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
        self.sellerlist = []
        self.buyerlist = []

        self.num_seller = 0
        self.num_buyer = self.num_agents

        self.populate(num_agents)

    def showMarketAgent(self):
        print('----------------------')
        for a in self.agentlist:
            print(a)
        print('Current Stock Price £' + str(self.book[-1]) + ' Existing market shares ' +str(self.shares))
        print('----------------------')

    def populate(self, n):

        # Create N agents
        for i in range(n):
            self.agentlist.append(ZeroIntelligentAgent(id=i+1, sellprice=initsellprice(), bidprice=initbidprice()))
            self.buyerlist = self.agentlist

    def record_order(self, tranction_price):
        self.book.append(tranction_price)
        self.stockprice = tranction_price

    def run(self):
        
        try:
            curr_agent = self.agentlist[random.randint(0,self.num_agents-1)]
        except IndexError as e:
            exit()

        # If the agent has one share
        if curr_agent.share: 

            if updateSellorBidPrice():
                curr_agent.sellprice -= 1

            if not self.num_buyer: # Hold
                self.record_order(self.stockprice)
                print('Cannot find suitable buyer... so Hold')
            
            else:

                index = -1
                maxBuy = 1
                for i,s in enumerate(self.agentlist):
                    if s.bidprice > maxBuy and not s.share:
                        index, maxBuy = i, s.bidprice
                print('Agent ' + str(index+1) + ' offers to buy the highest price £' + str(maxBuy))

               # if maxBuy < curr_agent.sellprice: #hold
                #    self.record_order(self.stockprice)
                 #   print('All bidprice is lower than the the sell price... so Hold')
                       
                #else:
                curr_buyer_agent = self.agentlist[index]
                print('Agent ' + str(curr_agent.id) + ' sell to Agent ' + str(index+1) + ' at price £' + str(maxBuy))
                tranction_price = maxBuy
                self.record_order(tranction_price)

                curr_agent.act(tranction_price)
                self.num_seller -= 1
                self.num_buyer += 1

                curr_buyer_agent.act(tranction_price)
                self.num_buyer -= 1
                self.num_seller += 1

        
        # If the agent has no share... 
        else:          
            # a) Update the price
            if updateSellorBidPrice():
                curr_agent.bidprice += 1

            # b)i If no one in the market sells, this agent is forced to buy at stock price
            if not self.num_seller:
                tranction_price = self.stockprice
                self.record_order(tranction_price)

                curr_agent.act(tranction_price)
                self.shares -= 1

                self.num_buyer -= 1
                self.num_seller += 1

                print('Agent ' + str(curr_agent.id) + ' buys at Market')
                

            # b)ii The agent looks for the lowest sell price among sellers and markets
            else:

                index = -1
                minSell = maxP
                for i,s in enumerate(self.agentlist):
                    if s.sellprice < minSell and s.share:
                        index, minSell = i, s.sellprice
                print('Agent ' + str(index+1) + ' offers to sell the lowest price £' + str(minSell))

                if self.stockprice < minSell and self.shares > 0:
                    # Buy from market
                    tranction_price = self.stockprice
                    self.record_order(tranction_price)    
                    curr_agent.act(tranction_price)
                    self.sellerlist.append(curr_agent)
                    
                    self.shares -= 1
                    self.num_buyer -= 1
                    self.num_seller += 1
                    print('Agent ' + str(curr_agent.id) + ' buys at Market')

                else:
                    # Buy from Sellers
                    curr_seller_agent = self.agentlist[index]
                    print('Agent ' + str(curr_agent.id) + ' buys from Agent ' + str(index+1) + ' at price £' + str(minSell))
                    
                    tranction_price = minSell
                    self.record_order(tranction_price)
                    
                    curr_agent.act(tranction_price)
                    self.num_buyer -= 1
                    self.num_seller += 1

                    curr_seller_agent.act(tranction_price)
                    self.num_seller += 1
                    self.num_buyer -= 1
                    #self.buyerlist.append(curr_seller_agent)

            self.showMarketAgent()

# Test 
def _test():
    m = Market(num_agents=20)
    print('+')
    print(m.agentlist)
    print(m.buyerlist)
    print(m.sellerlist)
    print('+')
    for i in range(1000):
        m.run()

    print(m.book)

    plt.plot(m.book)
    plt.show()

if __name__ == '__main__':
    _test()
    '''
    agentlist, buyerlist = [], []
    for i in range(10):
        agentlist.append(ZeroIntelligentAgent(id=i+1, sellprice=initsellprice(), bidprice=initbidprice()))
        buyerlist = agentlist

    a = buyerlist[0]
    a.id = -1 

    print(a, buyerlist[0], agentlist[0])

    a = buyerlist[5]
    a.id, a.sellprice, a.bidprice = -10, -10, -10
    print(a, buyerlist[5], agentlist[5])
            # Randomly select N/2 agent to hold one share
        #random.shuffle(self.agentlist)
        #for s,a in zip(range(self.shares), self.agentlist):
        #    a.act(0, reset=False)
        #random.shuffle(self.agentlist)
    '''