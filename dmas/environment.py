import sys
import random
import numpy as np
from tqdm import tqdm
sys.path.append('./')
import agent

class Environment:
    # attributes
    num_agents = None  # number of agents in the network
    num_liars = None  # number of liars (opinion = -1)
    num_experts = None  # number of liars (opinion = 1)
    num_connections = None  # the connectivity of the network TODO: change to something more elaborate
    num_news = None  # number of different news propagating in the network (=1 for now)
    num_steps = None  # how long the simulation will run TODO: use more elaborate termination criterion
    agent_list = None  # list of all agents
    connectivity_matrix = None  # keeps all the connections between agents in the network (row [HAS_CONNECTION_WITH] column)

    # initializer
    def __init__(self, num_agents, num_liars, num_experts, num_connections, num_news, num_steps):
        self.num_agents = num_agents
        self.num_liars = num_liars
        self.num_experts = num_experts
        self.num_connections = num_connections
        self.num_news = num_news
        self.num_steps = num_steps
        self.agent_list = self._generate_agents()
        self.connectivity_matrix = self._initalize_connecticity_matrix()


    # generates a list of the network's agents (private)
    def _generate_agents(self):
        list_of_agents = []
        for number in range(self.num_agents):
            list_of_agents.append(agent.Agent(0, random.uniform(0.0, 1.0)))
        # assign opinions to agents
        agent_indexes = random.sample(range(len(list_of_agents)), k=self.num_liars+self.num_experts)
        for a in agent_indexes[:self.num_liars]:
            list_of_agents[a].opinion = -1
        for a in agent_indexes[self.num_liars:]:
            list_of_agents[a].opinion = 1
        return list_of_agents


    # initalize connecticity matrix
    def _initalize_connecticity_matrix(self):
        connectivity_matrix = np.zeros((self.num_agents, self.num_agents))
        for number in range(self.num_connections):
            # randomly decide connection between 2 agents
            pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # repeat until pair is not already connected
            while connectivity_matrix[pair[0], pair[1]] == 1:
                pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # update matrix
            connectivity_matrix[pair[0], pair[1]] = 1
        return connectivity_matrix


    # communication protocol
    def agent_communication(self, agent_a, agent_b):
        if agent_a.opinion != agent_b.opinion:
            # determine winning opinion of the communication
            # neutral opinions do not spread, the other agent's opinion automatically wins
            if agent_a.opinion == 0:
                winner = 2  # opinion of agent_b is the outcome of discussion
            elif agent_b.opinion == 0:
                winner = 1  # opinion of agent_a is the outcome of discussion
            else:  # randomly decide winning opinion
                winner = random.randint(1, 2)
            # resolve agent acceptance
            if winner==1:
                agent_b.evaluate_opinion(agent_a.opinion)
            elif winner==2:
                agent_a.evaluate_opinion(agent_b.opinion)


    # printing stistics/results of simulation
    def simulations_stats(self):
        countTrue = 0
        countNeutral = 0
        countFalse = 0
        for agent in self.agent_list:
            if agent.opinion == 1:
                countTrue += 1
            if agent.opinion == 0:
                countNeutral += 1
            if agent.opinion == -1:
                countFalse += 1
        print(">> Number of True opinions : {0}".format(countTrue))
        print(">> Number of Neutral opinions : {0}".format(countNeutral))
        print(">> Number of False opinions : {0}".format(countFalse))
        print(">> Connectivity matrix:")
        print(self.connectivity_matrix)


    # initiates the simulation
    def run_simulation(self):
        print(">> Initial configurations:")
        self.simulations_stats()
        print("<< Beginning simulation >>")
        for step in tqdm(range(self.num_steps)):
            # print("- STEP: {0} of {1}".format(step+1, self.num_steps))
            # choose agent to communicate
            sender_index = random.randint(0, self.num_agents-1)  # randint is inclusive
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index!= sender_index)]
            receiver_index = random.randint(0, len(sender_phonebook))
            receiver = self.agent_list[receiver_index]
            self.agent_communication(sender, receiver)
        print("<< END OF SIMULATION >>")
        self.simulations_stats()

