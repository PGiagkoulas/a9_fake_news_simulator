import random
from statistics import mode


class Agent:
    # attributes
    opinion = None  # the current belief of the agent (-1: false, 0:neutral, 1: true) (can become a list later for multiple news)
    opinion_base = {}  # The opinions that the agent heard from other persons
    scepticism = None  # percent chance to change opinion when receives a different opinion

    # initializer
    def __init__(self, opinion, scepticism, num_agents):
        self.scepticism = scepticism
        self.opinion = opinion
        # the agent initially thinks every other agent is neutral until they get called by them
        self.opinion_base = {key: 0 for key in range(num_agents)}

    # evaluate new opinion from discussion
    def evaluate_opinion(self, new_opinion):
        # accept or not
        if random.uniform(0.0, 1.0) > self.scepticism:
            self.opinion = new_opinion

    def form_opinion(self):
        # if the agent is either a liar or an expert they are 'stubborn' and don't change their opinion at all
        if self.scepticism == 1:
            pass
        else:
            opinion_base = [value for value in self.opinion_base.values() if value != 0]
            # in case there is a tie between "true" and "false" information
            if opinion_base.count(1) == opinion_base.count(-1):
                # then the agent takes on the last opinion they heard with the probability of 1 - skepticism
                if random.uniform(0.0, 1.0) > self.scepticism:
                    self.opinion = -1 * self.opinion  # this flips the current opinion to the one that caused the tie
            # if there is no tie, we just take the mode
            else:
                self.opinion = mode(opinion_base)
