from utility import *
import random
import numpy as np
import scipy as sp

'''
# Template for designing Your agent
class DesignYourOwnAgent(Agent):

    def __init__(self, id):
        Agent.__init__(self,id)

    # Your information display in the market
    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '

    def newact(self, market):
        # Your action when you're selected at a time step
        # This method should return 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL/None), quantity(int)' 
    
    def record(self, direction, price, market, quantity=1):
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
        
    def record(self, direction, price, market, quantity=1):

        if direction: #If Sell
            self.share -= quantity
            self.sell_record.append(price)

        else:
            self.share += quantity
            self.buy_record.append(price)

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
        self.mu, self.sigma = 0, 2 
    
    def __str__(self):
        return '<0IQAgent %d owns %d share with sell price %f and bidprice %f>' % (self.id, self.share, self.sellprice, self.bidprice)


    # This Function needs clarifcation !!!!!!!!!!!
    def resetPrice(self,price, direction=None):
        
        swing = random.randint(0, 45)
        Pb = np.random.normal(price-swing, self.sigma)
        Ps = np.random.normal(price+swing, self.sigma)

        self.sellprice = Ps     #random.randint(price, maxP)
        self.bidprice = Pb      #random.randint(1, price)

        # Normal Skew Disdributtion

    def sell(self, market=None, quantity=None): 

        # Method return a tuple of (dealing buyer, the transaction price, number of shares)

        # Update its own bidPrice
        if self.updateSellorBidPrice():
            self.bidprice -= 1
        
        # Randomly select a number
        quantity = int(np.random.uniform(0, self.share)) + 1
        #print('Sell quant ' + str(quantity))
        print('Agent wants to sell ' + str(quantity) + ' shares')

        if not market.num_buyer: # If there's no buyer in the market
            # The agent cannot do anything but Hold
            print('There is no buyers in the market')
            return None, None, None

        else:
            # Find the agent with the highest bidprice
            index = -1
            maxBuy = 1
            for i,s in enumerate(market.agentlist):
                if s.bidprice > maxBuy:
                    index, maxBuy = i, s.bidprice

            #If the agent can find the agent with the highest bidprice

            if index is not -1:
                print('Agent ' + str(index+1) + ' offers to buy from ' +str(self.id)+' price with Quantity '+ str(quantity))

            if index+1 is self.id: # If the agent is itself, then skip it...
                #print('sell index', index, 'selfid',self.id)
                #input()
                print('The agent cannot trade with itself')
                return None, None, None

            elif index > -1 :
                # The agent cannot trade with itself
                # input()
                print('Agent ' + str(self.id) + ' hopes to sell to agent ' +str(index+1))
                curr_buyer_agent = market.agentlist[index]
                tranction_price = maxBuy

                return curr_buyer_agent, tranction_price, quantity

            else:
                #No suitable buying agent
                print('Cannot find a suitable buying agent')

                return None, None, None

    def buy(self, market=None, quantity=1):
        # a) Update the price
        if self.updateSellorBidPrice():
            self.bidprice += 1

        if not market.num_seller: # If no one in the market sells, then look for available shares in the market
            if market.shares <= quantity: # If there're encough nymber of shares in the market, purchase it, o
                print('No agent sells, so buy from market')
                #input()
                return 'market', market.stockprice
            else:
                print('No agent sells and No available market')
                return None, market.stockprice

        else:
            index = -1
            minSell = INFINITY
            for i,s in enumerate(market.agentlist):
                if s.sellprice < minSell and s.share >= quantity:
                    index, minSell = i, s.sellprice
            
            if index is not -1:
                print('Agent ' + str(index+1) + ' offers to sell to' +str(self.id)+' price £' + str(minSell) + ' with Quantity'+ str(quantity)+ ' (0 is the market)')

            # Buy at market
            if market.stockprice < minSell and market.shares >= quantity:
                print('The market has ' + str(quantity) + ' share and current stockprice is lower' + str(market.stockprice) )
                return None, market.stockprice
            
            elif index+1 is self.id:
                # The agent cannot trade with itself
                #print('BUY index', index, 'selfid',self.id)
                #input()
                print('The agent cannot trade with himself')
                return None, None

            elif index > -1:
                # Buy from Sellers
                print('Agent ' + str(self.id) + ' hopes to buy from agent ' +str(index+1))
                curr_seller_agent = market.agentlist[index]
                tranction_price = minSell
                return curr_seller_agent, tranction_price

            else:
                # No suitable conditions, contiune holding
                print('Agent ' + str(self.id) + 'cannot find a suitable agent')
                return None, None

    def newact(self, market):
        # If the agent has one share, the agent is a seller
        # Basic rules: If the agent has holding shares, the agent sells, otherwise the agent buys
        if self.share:
            direction = SELL
            current_buyer, transaction_price, q = self.sell(market=market, quantity=1)
            return current_buyer, transaction_price, direction, q

        else:
            quant = int(np.random.uniform(1, market.maxPurchase-1))
            print('This agent wants to buy shares quantity: '+ str(quant))
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

    def offer(self, price, quantity, direction, market):
        if probabilityGenerator(0.2):
            return False
        return True

    # Supportive functions        
    def initbidprice(self):
        #maxP = PickLastClosePrice()
        low = int(maxP/3)
        high = int(maxP/2)
        return round(np.random.uniform(low=low, high=high, size=None), 2)

    def initsellprice(self):
        self.maxP = PickLastClosePrice()
        low = int(self.maxP/2)
        high = int(self.maxP*2/3)
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
        ZeroIntelligentAgent.__init__(self, id)

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

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel, Matern

class NormalProcessAgent(Agent):
    def __init__(self, id):
        Agent.__init__(self,id)
        self.wealth = 0
        self.sellprice = self.initsellprice()
        self.bidprice = self.initbidprice()
        self.kernel = Matern(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
        self.predictor = GaussianProcessRegressor(kernel=self.kernel, n_restarts_optimizer=9)
        

    def __str__(self):
        return '<Gaussian Process Agent %d owns %d share with sell price %f and bidprice %f and Wealth $%s>' % (self.id, self.share, self.sellprice, self.bidprice, self.wealth)

    def newact(self, market):
        #input()
        if self.share == 0:
            # Buy at the market or agent with lowest sellPrice
            index, minSell = -1, maxP
            for i,s in enumerate(market.agentlist):
                if s.sellprice < minSell and s.share >= 1:
                    index, minSell = i, s.sellprice
            print('Agent ' + str(index+1) + ' offers to sell the lowest price £' + str(minSell) +' (0 is the market)')

            if index+1 == self.id:
                return NO_ACTION
            elif index > -1: #Possible agent
                if minSell < market.stockprice: # Buy from agent
                    # 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL/None), quantity(int)'
                    d = market.agentlist[index]
                    return d, d.sellprice, BUY, 1

                elif market.shares > 0: # Buy from market
                    return None, market.stockprice, BUY, 1
                else:
                    return NO_ACTION

            else:
                return NO_ACTION
        else:

            # Train the predictor
            if len(market.tradeSequence) > 10:
                #input()
                book = market.book[-30:]
                X, Y = self.create_ts(book, series=6)
                print(X.shape, Y.shape) # 16,6  16,1
                #input()
                self.trainPredictor(X,Y)
                #input()
                
                pre_proc = book[-7:] + [0]
                future, _ = self.create_ts(pre_proc, series=6)
                future = self.predictPredictor(future)

                future_value = np.exp(future[0])
                print(future_value)
                if future_value > market.stockprice:
                    direction = BUY
                    quantity = 1
                    if not market.num_seller: # If no one in the market sells, then look for available shares in the market
                        if market.shares <= quantity: # If there're encough nymber of shares in the market, purchase it, o
                            print('No agent sells, so buy from market')
                            return 'market', market.stockprice, direction, 1
                        else:
                            print('No agent sells and No available market')
                            return NO_ACTION
                    else:
                        index = -1
                        minSell = INFINITY
                        for i,s in enumerate(market.agentlist):
                            if s.sellprice < minSell and s.share >= quantity:
                                index, minSell = i, s.sellprice
                        
                        if index is not -1:
                            print('Agent ' + str(index+1) + ' offers to sell to' +str(self.id)+' price £' + str(minSell) + ' with Quantity'+ str(quantity)+ ' (0 is the market)')

                        # Buy at market
                        if market.stockprice < minSell and market.shares >= quantity:
                            print('The market has ' + str(quantity) + ' share and current stockprice is lower' + str(market.stockprice) )
                            return None, market.stockprice, direction, 1
                        
                        elif index+1 is self.id:
                            # The agent cannot trade with itself
                            #print('BUY index', index, 'selfid',self.id)
                            #input()
                            print('The agent cannot trade with himself')
                            return NO_ACTION

                        elif index > -1:
                            # Buy from Sellers
                            print('Agent ' + str(self.id) + ' hopes to buy from agent ' +str(index+1))
                            curr_seller_agent = market.agentlist[index]
                            tranction_price = minSell
                            return curr_seller_agent, tranction_price, direction, 1

                        else:
                            # No suitable conditions, contiune holding
                            print('Agent ' + str(self.id) + 'cannot find a suitable agent')
                            return NO_ACTION

                else:
                    if self.share > 0:
                        direction = SELL
                        quantity = 1

                        if not market.num_buyer: # If there's no buyer in the market
                            # The agent cannot do anything but Hold
                            print('There is no buyers in the market')
                            return NO_ACTION

                        else:
                            # Find the agent with the highest bidprice
                            index = -1
                            maxBuy = 1
                            for i,s in enumerate(market.agentlist):
                                if s.bidprice > maxBuy:
                                    index, maxBuy = i, s.bidprice

                            #If the agent can find the agent with the highest bidprice

                            if index is not -1:
                                print('Agent ' + str(index+1) + ' offers to buy from ' +str(self.id)+' price with Quantity '+ str(quantity))

                            if index+1 is self.id: # If the agent is itself, then skip it...
                                print('The agent cannot trade with itself')
                                return NO_ACTION

                            elif index > -1 :
                                # The agent cannot trade with itself
                                # input()
                                print('Agent ' + str(self.id) + ' hopes to sell to agent ' +str(index+1))
                                curr_buyer_agent = market.agentlist[index]
                                tranction_price = maxBuy

                                return curr_buyer_agent, tranction_price, direction, quantity

                            else:
                                #No suitable buying agent
                                print('Cannot find a suitable buying agent')

                                return NO_ACTION
                    else:
                        return NO_ACTION
             
            else:
                return NO_ACTION

    def offer(self, price, quantity, direction, market): 

        last_21days = market.book[-21:]
        _x, _ = NormalProcessAgent.create_ts(last_21days, series=6)
        future = np.exp(self.predictor.predict(_x)[0])

        if future > market.stockprice and direction is BUY:
            return True

        elif future < market.stockprice and direction is SELL:
            return False

        return False

    def record(self, direction, price, market, quantity=1):
        
        if direction is BUY:
            self.wealth -= price*quantity
            self.share += quantity
        elif direction is SELL:
            self.wealth += price*quantity
            self.share -= quantity
        else:
            pass

        self.resetPrice(price=price)

    @staticmethod
    def create_ts(ds, series=7):
        X, Y =[], []
        for i in range(len(ds)-series - 1):
            item = ds[i:(i+series)]
            X.append(item)
            Y.append(ds[i+series])
        return np.log(np.array(X)), np.log(np.array(Y)).reshape(-1,1)
    
    def trainPredictor(self, X, Y):
        self.predictor.fit(X,Y)

    def predictPredictor(self, X):
        return self.predictor.predict(X)

    def initbidprice(self):
        low = maxP/3
        high = maxP/2
        return round(np.random.uniform(low=low, high=high, size=None), 2)

    def initsellprice(self):
        low = maxP/2
        high = maxP*2/3
        return round(np.random.uniform(low=low, high=high, size=None), 2)

    def resetPrice(self,price, direction=None):
        
        swing = random.randint(0, 100)
        Pb = np.random.normal(price-swing, 0.8)
        Ps = np.random.normal(price+swing, 0.8)

        self.sellprice = Ps     #random.randint(price, maxP)
        self.bidprice = Pb      #random.randint(1, price)

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
    import matplotlib.pyplot as plt
    from scipy.stats import skewnorm
    from scipy.stats import skewnorm
    a = []
    mu, sigma = 1000, 1  
    one = np.random.normal(1000, sigma, size=1)
    for _ in range(1000):
        one = np.random.normal(mu, sigma)
        a.append(one)
    

    B = a
    print(B)
    plt.hist(B)
    plt.show()

    from sklearn.gaussian_process import GaussianProcessRegressor
    from sklearn.gaussian_process.kernels import RBF, ConstantKernel, Matern
    import random 
    a = list(range(10))
    a = np.array(a)
    print(a)
    kernel = Matern(1.0, (1e-3, 1e3)) * RBF(10, (1e-2, 1e2))
    predictor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9)
    
    trainX, trainY = NormalProcessAgent.create_ts(a, series=4)
    print(trainX)
    print(trainY)
    predictor.fit(trainX, trainY)
    test = predictor.predict([a[-4::]])
    print(test)