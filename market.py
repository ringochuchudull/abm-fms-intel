from utility import *
from agent import *
import random
import matplotlib.pyplot as plt


class Market():

    '''
    An abstract Market Class to describe and simulate a real world market


    attributes:
    num_agents(Integer): Denotes number of agents in the market
    shares(Integer): Denotes number of available shares within the market
    stockprice(float32): Indicates the current stockprice of the good
    book(list/Dynamic array): A list to store all historic stockprices
    num_seller(Integer): Number of sellers in the market
    num_buyer(Integer): Number of buyer in the marker
    steps(Integer): Number of iterateration this market will run

    Function:
    -populate(n="number_agent(int)"): Initate the market by creating N agents, only runs once
    -record_order(trancation_price): Record down the new stock price by adding the current stock price to 'book(list)' and 
        update 'stockprice(float32)
    -newtrade(): Rules/ Simulating a trade by 1) Randoming selecting an agent; 2) Trade decision and action taken by   
        the agent 3) Update 'book(list)' and 'stockprice(Integer)'
    -run(): Running N times of newtrade(), where N equals to ;steps(Integer)'        
    -showMarketAgent(): Print all agents states in the market
    -plotStockTrend(): Plot the stock price
    '''

    def __init__(self, num_agents, steps):

        self.num_agents = num_agents
        self.shares = int(num_agents/2)
        
        self.stockprice = int(maxP/1.65)
        self.book = []

        self.agentlist = []

        self.num_seller = 0
        self.num_buyer = self.num_agents
        self.steps = steps

        self.populate(num_agents)
        

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
                # If there is noone willing to buy the share from curr_agent, then...
                self.record_order(self.stockprice)
                print('Cannot find suitable buyer... so Hold')
            else:
                # If there is someone willing to buy the share
                self.num_seller -= 1
                self.num_buyer += 1
                # Update the market stockprice
                self.record_order(transaction_price)

                # Update the record of curr_agent's dealer
                dealer.record(BUY, transaction_price)
                self.num_buyer -= 1
                self.num_seller += 1

                print('Agent ' + str(dealer.id) + ' offers to buy the highest price £' + str(transaction_price))
                print('Agent ' + str(curr_agent.id) + ' sell to Agent ' + str(dealer.id) + ' at price £' + str(transaction_price))
                      
        elif direction is BUY:

                # If nobody sells or lowest sellprice is lower than stockprice, buy from market
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

                    # Update the market stockprice
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
        print('-------------------------------------')
        for a in self.agentlist:
            print(a)
        print('Current Stock Price £' + str(self.book[-1]) + ' Existing market shares ' +str(self.shares))
        print('-----------------------------------')

    def plotStockTrend(self):
        plt.plot(self.book)
        plt.show()

# Test 
def _test():
    m1.plotStockTrend()


if __name__ == '__main__':
    _test()
