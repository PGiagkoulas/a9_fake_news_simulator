import random
from statistics import mode

class Agent:

    # attributes
    opinion = None  # the current belief of the agent (-1: false, 0:neutral, 1: true) (can become a list later for multiple news)
    scepticism = None  # percent chance to change opinion when receives a different opinion

    # initializer
    def __init__(self, opinion, scepticism):
        self.scepticism = scepticism
        self.opinion = opinion


    # evaluate new opinion from discussion
    def evaluate_opinion(self, new_opinion):
        # accept or not
        if random.uniform(0.0, 1.0) > self.scepticism:
            self.opinion = new_opinion