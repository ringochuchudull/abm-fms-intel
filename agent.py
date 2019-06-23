from utility import *
import random

class Agent:

    def __init__(self, id):
        self.id = id 
        self.share = 0 #Also detemine whether he is a buyer or seller

        self.sell_record = []
        self.buy_record = []

    def __str__(self):
        return '<Agent ' + str(self.id) + ' > '
        
    def record(self, direction, trans_price, quantity=1):

        if direction: #If Sell
            self.share -= quantity
            self.sell_record.append(trans_price)

        else:
            self.share += quantity
            self.buy_record.append(trans_price)

    def newact(self, price):
        # Implementated in subclass accordingly to types of agents

        # This method should return 'dealer(Agent Object)', 'transaction_price(int)' 'direction(BUY/SELL)' 
        raise Exception('No implementation')

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

            curr_buyer_agent = market.agentlist[index]
            tranction_price = maxBuy

            return curr_buyer_agent, tranction_price
     
    
    def buy(self, market=None):
        # a) Update the price
        if updateSellorBidPrice():
            self.bidprice += 1

        if not market.num_seller:
            print('haha')
            return None, market.stockprice

        else:

            index = -1
            minSell = maxP
            for i,s in enumerate(market.agentlist):
                if s.sellprice < minSell and s.share:
                    index, minSell = i, s.sellprice
            print('Agent ' + str(index+1) + ' offers to sell the lowest price £' + str(minSell))

            # Buy at market
            if market.stockprice < minSell and market.shares > 0:
                return None, market.stockprice

            else:
                # Buy from Sellers
                curr_seller_agent = market.agentlist[index]
                tranction_price = minSell
                return curr_seller_agent, tranction_price

    def record(self, direction, price, quantity=1, reset=True):
        
        if direction: #If Sell
            self.share -= quantity
            self.sell_record.append(price)

        else:
            self.share += quantity
            self.buy_record.append(price)

        if reset:
            print('reset price')
            self.resetPrice(int(price))
        
    def newact(self, market):

        if self.share:
            direction = SELL
            current_buyer, transaction_price = self.sell(market=market)
            if current_buyer is not None:
                self.record(SELL, transaction_price)
            return current_buyer, transaction_price, direction
        
        else:
            direction = BUY
            current_seller, transaction_price = self.buy(market=market)
            self.record(BUY, transaction_price)
            return current_seller, transaction_price, direction

# Test 
if __name__ == '__main__':
    pass