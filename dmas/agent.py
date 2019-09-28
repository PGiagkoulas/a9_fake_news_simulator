import random
from statistics import mode

class Agent:

    # attributes
    opinion = None  # the current belief of the agent (-1: false, 0:neutral, 1: true) (can become a list later for multiple news)
    opinion_base = []  # The opinions that the agent heard from other persons
    scepticism = None  # percent chance to change opinion when receives a different opinion

    # initializer
    def __init__(self, opinion, scepticism):
        self.scepticism = scepticism
        self.opinion = opinion


    # evaluate new opinion from discussion
    def evaluate_opinion(self, new_opinion):
        # accept or not
        if random.uniform(0.0, 1.0) > self.sceptisicm:
            self.opinion = new_opinion

    def form_opinion(self):
        # if the agent is either a liar or an expert they are 'stubborn' and don't change their opinion at all
        if self.sceptisicm == 1:
            pass
        # in case there is a tie between "true" and "false" information
        if self.opinion_base.count(1) == self.opinion_base.count(-1):
            # then the agent takes on the last opinion they heard with the probability of 1 - skepticism
            if random.uniform(0.0, 1.0) > self.sceptisicm:
                self.opinion = self.opinion_base[-1]
        # if there is no tie, we just take the mode
        else:
           self.opinion = mode(self.opinion_base)
