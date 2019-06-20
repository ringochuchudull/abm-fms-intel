from utility import *
from agent import *
import random


class Market():
    def __init__(self, num_agents):
        self.shares = int(num_agents/2)
        self.sellbook = []
        self.buybook = []
        self.agentlist = []
        self.populate(num_agents)

    def populate(self, n):
        for i in range(n):
            self.agentlist.append(ZeroIntelligentAgent(i+1))

# Test 
if __name__ == '__main__':
    m = Market(num_agents=10)
    print(m.agentlist[0])