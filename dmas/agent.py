import random

class Agent:

    # attributes
    opinion = None  # the current belief of the agent (-1: false, 0:neutral, 1: true) (can become a list later for multiple news)
    sceptisicm = None  # percent chance to change opinion when receives a different opinion

    # initializer
    def __init__(self, opinion, naivete):
        self.sceptisicm = naivete
        self.opinion = opinion


    # evaluate new opinion from discussion
    def evaluate_opinion(self, new_opinion):
        # accept or not
        if random.uniform(0.0, 1.0) > self.sceptisicm:
            self.opinion = new_opinion