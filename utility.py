import numpy as np

BUY  = 0
SELL = 1
HOLD = -1

maxP = 2000
minP = 1

INFINITY = float('inf')
draft_param = 0.3

NO_ACTION = (None, None, None, None)

# A function returning a True with Probability
def probabilityGenerator(boundary=0.25):
    a = np.random.uniform(low=0, high=1)
    if a < boundary:
        return True
    return False

if __name__ == '__main__':
    print('You re in the utility file')
    pass