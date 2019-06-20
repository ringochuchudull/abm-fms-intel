from utility import *
import random

class Agent:

    def __init__(self, id):
        self.id = id 
        self.share = 0 

    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '
        
    def act(self, price):
        # Implementated in subclass accordingly to types of agents
        raise Exception('No implementation')

    def record(self, direction, quantity=1):
        '''
        Record transaction
        '''
        print('check direction', direction)
        
        if direction: #If Sell
            self.share -= quantity
        else:
            self.share += quantity


class ZeroIntelligentAgent(Agent):
    def __init__(self, id):
        Agent.__init__(self,id, sellprice=maxP, bidprice=1)
        self.sellprice = 0
        self.bidprice = 0
    
    def __str__(self):
        return '<Agent %d with sell price %f and bidprice %f>' % (self.id, self.sellprice, self.bidprice)

    def resetPrice(self,price):
        self.bidprice = random.randint(1,price)
        self.sellprice = random.randint(price, maxP)
        
    def act(self, price):
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
        self.resetPrice(price)

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