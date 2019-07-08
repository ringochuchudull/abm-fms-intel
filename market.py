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
    maxPurcase(Integer): Max purchasing number of shares
    minPurchase(Integer): Min number of purchasing shares
    tradeSequence(String): A string records each market action. 1:SELL, 0:BUY, #:HOLD

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
        
        # Initial Stock Price
        self.stockprice = int(maxP/1.65)
        
        # An array to keep trace of all transaction price
        self.book = []

        # An array to keep records of all agents in the market
        self.agentlist = []

        self.num_seller = 0
        self.num_buyer = self.num_agents

        # Number of timesteps
        self.steps = steps

        # Maximum number of purchases
        self.maxPurchase = int(self.shares/2)
        self.minPurchase = 1

        # A String to record buy Sell or hold
        self.tradeSequence = ''

        # initialize the market with agents
        self.populate(num_agents)

    def populate(self, n):
        # Create N agents
        for i in range(n):
            if probabilityGenerator(0.7):
                if probabilityGenerator(0.3):
                    self.agentlist.append(ImitatingAgentV2(id=i+1))
                else:
                    self.agentlist.append(ZeroIntelligentAgent(id=i+1))
            else:
                self.agentlist.append(NormalProcessAgent(id=i+1))
        # self.agentlist.append(ZeroIntelligentAgent(id=i + 1, sellprice=initsellprice(), bidprice=initbidprice()))

        self.buyerlist = self.agentlist

    def record_order(self, tranction_price):
        self.book.append(tranction_price)
        self.stockprice = tranction_price

    @staticmethod
    def autoregressiveprocess1(dtminus1, wt): # Auto progressive of order 1
        return 10+ 0.95*(dtminus1 - 10)+ wt

    def releaseDividend(self,dMinusOne): 
        '''
        In the company of this stock earns money, the company release profit to shareholder
        '''
        pass

    # Describe the function of the specialist’s in the market
    def newtrade(self):
        
        # A random agent is selected, this agent will act to choose who to trade, the price, BUY/SELL/HOLD and amount of shares
        curr_agent = self.agentlist[random.randint(0,self.num_agents-1)]
        dealer, transaction_price, direction, quantity = curr_agent.newact(market=self)

        if direction is SELL:

            if dealer is None:
                # If there is noone willing to buy the share from curr_agent, then...
                self.record_order(self.stockprice)
                print('Cannot find suitable buyer... so Hold')
                self.tradeSequence += '#'

            else:
                # If there is someone willing to buy the share, the market sends the offer to the dealer
                # If the dealer accepts the offer (Returning a true), the market proceed to update
                if dealer.offer(direction=BUY, price=transaction_price, quantity=quantity):
                    # Update the market stockprice
                    self.record_order(transaction_price)

                    # Update the record of curr_agent's dealer
                    curr_agent.record(direction=SELL, price=transaction_price, market=self, quantity=quantity)
                    self.num_seller -= 1
                    self.num_buyer += 1

                    dealer.record(direction=BUY, price=transaction_price, market=self, quantity=quantity)
                    self.num_buyer -= 1
                    self.num_seller += 1

                    print('Agent ' + str(dealer.id) + ' offers to buy the highest price £' + str(transaction_price))
                    print('Agent ' + str(curr_agent.id) + ' sell to Agent ' + str(dealer.id) + ' at price £' + str(transaction_price))

                    self.tradeSequence += '1'
                else:
                    print('Offer declined')
                    self.record_order(self.stockprice)
                    self.tradeSequence += '#'

        elif direction is BUY:

                # If nobody sells or lowest sellprice is lower than stockprice, buy from market
                if dealer is None and self.shares >= quantity:
                    curr_agent.record(direction=BUY, price=transaction_price, market=self, quantity=quantity)
                    self.record_order(self.stockprice)
                    self.shares -= quantity

                    self.num_buyer -= 1
                    self.num_seller += 1
                    print('Agent ' + str(curr_agent.id) + ' buys from Market')
                    self.tradeSequence += '0'

                elif dealer is not None: # There is a suitable dealer

                    # Ask the dealer whether to accept
                    if dealer.offer(direction=SELL, price=transaction_price, quantity=quantity):
                        self.record_order(transaction_price)
                        curr_agent.record(direction=BUY, price=transaction_price, market=self, quantity=quantity)
                        self.num_buyer -= 1
                        self.num_seller += 1

                        # Update the market stockprice
                        dealer.record(direction=SELL, price=transaction_price, market=self, quantity=quantity)
                        self.num_seller -= 1
                        self.num_buyer += 1

                        print('Agent ' + str(curr_agent.id) + ' buys from Agent ' + str(dealer.id) + ' at price £' + str(transaction_price))
                        self.tradeSequence += '0'

                    else:
                        # If the dealer declines:
                        print('The dealer refuse to sell')
                        self.record_order(self.stockprice)
                        self.tradeSequence += '#'
                else:
                    # Dealer is None and Market do not have enough share
                    self.tradeSequence += '#'
        else:
            print('Neither Buy nor Sell')
            self.tradeSequence += '#'
            self.record_order(self.stockprice)
            
        self.showMarketAgent()


    def run(self):
        for _ in range(self.steps):
            self.newtrade()
            #input()

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
    pass

if __name__ == '__main__':
    _test()
