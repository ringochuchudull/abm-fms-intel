from utility import *
import random

class Agent:

    def __init__(self, id):
        self.id = id 
        self.share = 0 #Also detemine whether he is a buyer or seller

    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '
        
    def act(self, price):
        # Implementated in subclass accordingly to types of agents
        raise Exception('No implementation')

    def record(self, direction, quantity=1):

        if direction: #If Sell
            self.share -= quantity
        else:
            self.share += quantity


class ZeroIntelligentAgent(Agent):
    def __init__(self, id, sellprice=maxP, bidprice=1):
        Agent.__init__(self,id)
        self.sellprice = sellprice
        self.bidprice = bidprice
    
    def __str__(self):
        return '<Agent %d owns %d share with sell price %f and bidprice %f>' % (self.id, self.share, self.sellprice, self.bidprice)

    def resetPrice(self,price):
        self.bidprice = random.randint(1,price)
        self.sellprice = random.randint(price, maxP)
        
    def sell(self, market=None):
        if updateSellorBidPrice():
            self.sellprice -= 1

        if not market.num_buyer:
            market.record_order(market.stockprice)
            return None, None

        else:
            index = -1
            maxBuy = 1
            for i,s in enumerate(market.agentlist):
                if s.bidprice > maxBuy and not s.share:
                    index, maxBuy = i, s.bidprice

            #if maxBuy < curr_agent.sellprice: #hold
                #self.record_order(self.stockprice)
                #print('All bidprice is lower than the the sell price... so Hold') 
            #else:

            curr_buyer_agent = market.agentlist[index]
            tranction_price = maxBuy
            self.act(tranction_price)

            return curr_buyer_agent, tranction_price
     
    
    def buy(self, market=None):
        # a) Update the price
        if updateSellorBidPrice():
            self.bidprice += 1

        # b)i If no one in the market sells, this agent is forced to buy at stock price
        if not market.num_seller:
            self.act(market.stockprice)
            return None, None
            '''
            tranction_price = market.stockprice
            market.record_order(tranction_price)


            market.shares -= 1

            market.num_buyer -= 1
            market.num_seller += 1

            print('Agent ' + str(self.id) + ' buys at Market')
            '''

        # b)ii The agent looks for the lowest sell price among sellers and markets
        else:

            index = -1
            minSell = maxP
            for i,s in enumerate(market.agentlist):
                if s.sellprice < minSell and s.share:
                    index, minSell = i, s.sellprice
            print('Agent ' + str(index+1) + ' offers to sell the lowest price £' + str(minSell))

            if market.stockprice < minSell and market.shares > 0:
                # Buy from market
   
                self.act(market.stockprice)
                return None, None
                '''
                tranction_price = market.stockprice
                market.record_order(tranction_price) 
                market.shares -= 1

                market.num_buyer -= 1
                market.num_seller += 1
                print('Agent ' + str(self.id) + ' buys at Market')
                '''
            else:
                # Buy from Sellers
                curr_seller_agent = market.agentlist[index]
                #print('Agent ' + str(self.id) + ' buys from Agent ' + str(index+1) + ' at price £' + str(minSell))
                
                tranction_price = minSell
                self.act(tranction_price)

                return curr_seller_agent, tranction_price
                '''
                market.record_order(tranction_price)
                

                market.num_buyer -= 1
                market.num_seller += 1

                curr_seller_agent.act(tranction_price)
                market.num_seller -= 1
                market.num_buyer += 1
                '''

    def act(self, price, reset=True):
        '''
        If the agent has one share, the agent sell,
        If the agent has no share, the agent buy
        '''
        if self.share:
            # Sell the share w
            self.record(SELL)
        else:
            self.record(BUY)
        
        # Reset the price randomly
        if reset:
            self.resetPrice(int(price))

    def update(prob):
        pass

# Test 
if __name__ == '__main__':
    pass