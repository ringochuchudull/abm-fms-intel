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
        '''
        Record transaction
        '''
        
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
            self.resetPrice(price)

    def update(prob):
        pass
# Test 
if __name__ == '__main__':
    a = Agent(0)
    print(a)
    print(BUY, SELL)
    b = ZeroIntelligentAgent(1, 2000, 1)
    b.act(12)
    print('share',b.share, b.sellprice, b.bidprice)
    b.act(12)
    print('share',b.share, b.sellprice, b.bidprice)

    test = [Agent(0), Agent(1), Agent(2), Agent(3)]
    buyer = [test[0], test[1] ]
    seller = [test[2],test[3] ]
    print('+')
    print(test)
    print(buyer)
    print(seller)
    print('+')

    buyer.remove(test[0])
    
    print('+')
    print(test)
    print(buyer)
    print(seller)
    print('+')