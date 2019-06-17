import matplotlib.pyplot as plt
import itertools
import random
import copy

class stock_market:
        def __init__(self, n_node, empty_ratio, similarity_threshold, n_iterations, races = 2):
            self.n_node = n_node 
            self.empty_ratio = empty_ratio
            self.agents = {}