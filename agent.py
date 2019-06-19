from utility import *

class Agent:

    '''
    Abstract agent class but implementing zero-intelligent agents

    Any agent class and its subclass MUST provide
    - a money attribute (float)
    - a stocks attribute (int)

    Any agent class and its subclass has act() method
    The agent returns a tuple of either:
    (direction) | (direction, price) | (direction, price, quantity)
    where direction is an int, 0 for buy and 1 for sell; price is 0.2  float of the good and quantity is an int

    Any agent class and its subclass has record() method

    Each agent can owns one share at most
    '''

    def __init__(self, id):
        self.id = id

    def __str__(self):

        return '<Agent ' + str(self.id) + ' > '
        

    def act(self):
        '''
        Implementated in subclass
        '''
        raise Exception('No implementation')

    def record(self, direction, price, quantity=1):
        """
        Record transaction
        """
        if direction:
            self.stocks -= quantity
            self.money += quantity*price
        else:
            self.stocks += quantity
            self.money -= quantity*price


class ZeroIntelligentAgent(Agent):
    def __init__(self, id, sellprice, bidprice):
        Agent.__init__(self,id)
        self.sellprice = sellprice
        self.bidprice = bidprice
    
    def __str__(self):
        return '<Agent %d with sell price %f and bidprice %f>' % (self.id, self.sellprice, self.bidprice)


# Test 
if __name__ == '__main__':
    a = Agent(0)
    print(a)
    b = ZeroIntelligentAgent(1, 2000, 1)
    print(b)
