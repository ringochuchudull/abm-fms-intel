from utility import *
import random
import numpy as np #np.exp

'''
# Template for designing Your agent
class DesignYourOwnAgent(Agent):

    def __init__(self, id):
        Agent.__init__(self,id)

    # Your information display in the market
    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '

    def newact(self):
        # Your action when you're selected at a time step
        # This method should return 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL/None), quantity(int)' 
    
    def record(self, direction, trans_price, market, quantity=1):
        # Update your internal state using this method
    
    def offer(self, price, quantity, direction):
        # You receive an offer from and agent.

        # e.g  offer(£100, 5, BUY) means the other agent invite you to BUY 5 shares at 100 pound
        #      offer(£80, 3, SELL) means the other agent kindly ask you to sell 3 shares at 80 pound
        # return True to accept the offer, False to decline 
'''

# Super Class
class Agent:

    '''
    An abstract agent class that allows itself to updates its state and react
    record(): Change the amount the shares holding and record the new price
    act(): Simulation of a trading decision
    '''
    def __init__(self, id):
        self.id = id 
        self.share = 0 #Also detemine whether he is a buyer or seller

        self.sell_record = []
        self.buy_record = []

    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '
        
    def record(self, direction, trans_price, market=None, quantity=1):

        if direction: #If Sell
            self.share -= quantity
            self.sell_record.append(trans_price)

        else:
            self.share += quantity
            self.buy_record.append(trans_price)

    def newact(self):
        # Implementated in subclass accordingly to types of agents
        # This method should return 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL), qua' 
        raise Exception('No implementation')

    def offer(self, price, quantity, direction):
        # When receive an offer from another agent,
        # return True to accept, false to decline
        raise Exception('No implementation')

    def profit(self):
        return sum(self.sell_record) - sum(self.buy_record)

# Sub Class
class ZeroIntelligentAgent(Agent):
    def __init__(self, id, sellprice=maxP, bidprice=1):
        Agent.__init__(self,id)
        self.sellprice = self.initsellprice()
        self.bidprice = self.initbidprice()
    
    def __str__(self):
        return '<0IQAgent %d owns %d share with sell price %f and bidprice %f>' % (self.id, self.share, self.sellprice, self.bidprice)

    def resetPrice(self,price, direction=None):
        self.sellprice = random.randint(price, maxP)
        self.bidprice = random.randint(1, price)

    def sell(self, market=None, quantity=None): 

        # Method return a tuple of (dealing buyer, the transaction price, number of shares)

        # Update its own bidPrice
        if self.updateSellorBidPrice():
            self.bidprice -= 1
        
        # Randomly select a number
        quantity = int(np.random.uniform(0, self.share)) + 1
        #print('Sell quant ' + str(quantity))


        if not market.num_buyer: # If there's no buyer in the market
            # The agent cannot do anything but Hold
            return None, None, None

        else:
            # Find the agent with the highest bidprice
            index = -1
            maxBuy = 1
            for i,s in enumerate(market.agentlist):
                if s.bidprice > maxBuy:
                    index, maxBuy = i, s.bidprice

            #If the agent can find the agent with the highest bidprice
            
            if index+1 is self.id: # If the agent is itself, then skip it...
                #print('sell index', index, 'selfid',self.id)
                #input()
                return None, None, None

            elif index > -1 :
                # The agent cannot trade with itself
                # input()
                curr_buyer_agent = market.agentlist[index]
                tranction_price = maxBuy
                return curr_buyer_agent, tranction_price, quantity

            else:
                #No suitable agent
                return None, None, None

    def buy(self, market=None, quantity=1):
        # a) Update the price
        if self.updateSellorBidPrice():
            self.bidprice += 1

        if not market.num_seller: # If no one in the market sells, then look for available shares in the market
            if market.shares <= quantity: # If there're encough nymber of shares in the market, purchase it, o
                print('No one sells, buy from market')
                return 'market', market.stockprice
            else:
                return None, market.stockprice

        else:
            index = -1
            minSell = maxP
            for i,s in enumerate(market.agentlist):
                if s.sellprice < minSell and s.share >= quantity:
                    index, minSell = i, s.sellprice
            print('Agent ' + str(index+1) + ' offers to sell the lowest price £' + str(minSell) +' (0 is the market)')

            # Buy at market
            if market.stockprice < minSell and market.shares >= quantity:
                return None, market.stockprice
            
            elif index+1 is self.id:
                # The agent cannot trade with itself
                #print('BUY index', index, 'selfid',self.id)
                #input()
                return None, None

            elif index > -1:
                # Buy from Sellers
                curr_seller_agent = market.agentlist[index]
                tranction_price = minSell
                return curr_seller_agent, tranction_price

            else:
                # No suitable conditions, contiune holding
                return None, None

    def newact(self, market):
        # If the agent has one share, the agent is a seller
        # Basic rules: If the agent has holding shares, the agent sells, otherwise the agent buys
        if self.share:
            direction = SELL
            current_buyer, transaction_price, q = self.sell(market=market, quantity=1)
            return current_buyer, transaction_price, direction, q

        else:
            quant = int(np.random.uniform(1, market.maxPurchase))
            print('buying quant'+ str(quant))
            direction = BUY
            current_seller, transaction_price = self.buy(market=market, quantity=quant)
            return current_seller, transaction_price, direction, quant

    def record(self, direction, price, market=None, quantity=1, reset=True):

        if direction:  # If Sell
            self.share -= quantity
            self.sell_record.append(price)

        else:
            self.share += quantity
            self.buy_record.append(price)

        if reset:
            #print('reset price')
            self.resetPrice(int(price), direction)

    def offer(self, price, quantity, direction):
        if probabilityGenerator(0.2):
            return False
        return True

    # Supportive functions        
    def initbidprice(self):
        low = maxP/3
        high = maxP/2
        return round(np.random.uniform(low=low, high=high, size=None), 2)

    def initsellprice(self):
        low = maxP/2
        high = maxP*2/3
        return round(np.random.uniform(low=low, high=high, size=None), 2)

    def updateSellorBidPrice(self):
        dd = (1+draft_param)/2
        d = np.random.uniform(low=0.0, high=1.0)
        if d < dd: # Approach to dP
            return True
        else: # Step awat from dp
            return False

# Subclass of ZeroIntelligentAgent, the only difference is this agent copies bid and sell price from random agent
class ImitatingAgentV2(ZeroIntelligentAgent):
    def __init__(self, id, sellprice=maxP, bidprice=1):
        ZeroIntelligentAgent.__init__(self, id, sellprice, bidprice)
        self.sellprice = sellprice
        self.bidprice = bidprice

    def __str__(self):
        return '<ImitatingQAgent %d owns %d share with sell price %f and bidprice %f>' % (
        self.id, self.share, self.sellprice, self.bidprice)

    def resetPrice(self, market=None):
        if self.share > 0:
            # Case as of a Potential Seller
            temp = []
            temp = [a for a in market.agentlist if a.share]
            random.shuffle(temp)
            tempAgent = temp[0]
            self.sellprice = tempAgent.sellprice

        elif not self.share:
            # Case as of a potential buyer
            temp = []
            temp = [a for a in market.agentlist if not a.share]
            random.shuffle(temp)
            tempAgent = temp[0]
            self.bidprice = tempAgent.bidprice

    def record(self, direction, price, market=None, quantity=1, reset=True):

        if direction:  # If Sell
            self.share -= quantity
            self.sell_record.append(price)

        else:
            self.share += quantity
            self.buy_record.append(price)

        if reset:
            #print('reset price')
            self.resetPrice(market=market)


class PalamAgent(Agent):
    def __init__(self, id, sellprice=maxP, bidprice=1):
        Agent.__init__(self,id)
        self.sellprice = sellprice
        self.bidprice = bidprice
        self.wealth = 1300

    def __str__(self):
        return '<ImitatingAgent %d owns %d share with sell price %f and bidprice %f and sequence %s>' % (self.id, self.share, self.sellprice, self.bidprice, self.tradeSequence)

    # The agent maxises this expetation value of the utility function
    def CARA(self, w, lambdaparam=0.5):
        return -np.exp(-lambdaparam*w)


    def autoregressiveprocess1(self, dtminus1, wt): # Auto progressive of order 1
        return 10+ 0.95*(dtminus1 - 10)+ wt

    # Must Implement
    def record(self, direction, trans_price, market=None, quantity=1):
        '''
        Will be called once after transaction in the market
        This function aims to change the internal state
        '''
        pass

    # Must implement
    def newact(self):
        # This method should return 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL)'
        pass


# Test
if __name__ == '__main__':
    pass