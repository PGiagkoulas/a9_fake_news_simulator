import sys
import random
import numpy as np
import pandas as pd
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
    communication_protocol = None  # determines how agents choose whom to call
    conversation_protocol = None  # determines how a conversation takes place and how agents change their opinion

    # initializer
    def __init__(self,
                 num_agents,
                 num_liars,
                 num_experts,
                 num_connections,
                 num_news,
                 num_steps,
                 communication_protocol="random",
                 conversation_protocol="battle_discussion"):
        self.num_agents = num_agents
        self.num_liars = num_liars
        self.num_experts = num_experts
        self.num_connections = num_connections
        self.num_news = num_news
        self.num_steps = num_steps
        self.agent_list = self._generate_agents()
        self.connectivity_matrix = self._initialize_connectivity_matrix()
        self.communication_protocol = communication_protocol
        self.conversation_protocol = conversation_protocol

    # generates a list of the network's agents (private)
    def _generate_agents(self):
        list_of_agents = []
        for number in range(self.num_agents):
            # agents are initially generated neutral and
            # their scepticism follows a normal distribution around the average scepticism level
            list_of_agents.append(agent.Agent(0, random.gauss(0.5, 0.1), self.num_agents))
        # assign opinions to agents
        agent_indexes = random.sample(range(len(list_of_agents)), k=self.num_liars + self.num_experts)
        # declare liars & experts
        # they will not change their opinion (scepticism = 1)
        for a in agent_indexes[:self.num_liars]:
            list_of_agents[a].opinion = -1
            list_of_agents[a].scepticism = 1
        for a in agent_indexes[self.num_liars:]:
            list_of_agents[a].opinion = 1
            list_of_agents[a].scepticism = 1
        return list_of_agents

    # initialize connectivity matrix
    def _initialize_connectivity_matrix(self):
        connectivity_matrix = np.zeros((self.num_agents, self.num_agents))
        for i in range(len(connectivity_matrix)):
            # guarantee that every agent is in at least one phonebook by someone else
            neighbour = i
            while neighbour == i:
                neighbour = np.random.randint(low=0, high=self.num_agents)
            connectivity_matrix[neighbour, i] = 1
            self.num_connections -= 1
        for number in range(self.num_connections):
            # randomly decide connection between 2 agents
            pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # repeat until pair is not already connected
            while connectivity_matrix[pair[0], pair[1]] == 1:
                pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # update matrix
            connectivity_matrix[pair[0], pair[1]] = 1
        return connectivity_matrix

    # conversation protocol
    def agent_conversation(self, agent_a, agent_b):
        if self.conversation_protocol == "battle_discussion":
            # agent_a is the sender and agent_b the receiver
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
                if winner == 1:
                    agent_b.evaluate_opinion(agent_a.opinion)
                elif winner == 2:
                    agent_a.evaluate_opinion(agent_b.opinion)
                self.exchange_phonebooks(agent_a, agent_b)
        elif self.conversation_protocol == "majority_opinion":
            # agent_a is the sender and agent_b the receiver
            # neutral opinions don't spread
            if agent_a.opinion != 0:
                agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
                agent_b.form_opinion()
            self.exchange_phonebooks(agent_a, agent_b)

    # printing statistics/results of simulation
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
        return countTrue, countNeutral, countFalse

    # exchange of phonebooks/connectivity matrix update
    def exchange_phonebooks(self, agent_a, agent_b):
        # retrieve indexes of the two agents
        index_a = self.agent_list.index(agent_a)
        index_b = self.agent_list.index(agent_b)
        # retrieve their individual phonebooks
        phonebook_a = self.connectivity_matrix[index_a, :]
        phonebook_b = self.connectivity_matrix[index_b, :]
        # take their union
        union_phonebook = [(connection if connection < 1 else 1) for connection in phonebook_a+phonebook_b]
        # update connectivity matrix
        self.connectivity_matrix[index_a, :] = union_phonebook
        self.connectivity_matrix[index_b, :] = union_phonebook
        # make certain no connection is made from the agents to themselves
        self.connectivity_matrix[index_a, index_a] = 0
        self.connectivity_matrix[index_b, index_b] = 0


    def run_communication_protocol(self):
        if self.communication_protocol == "random":
            # choose agent to communicate
            # create set of agents who have an outgoing connections
            valid_senders = [index for index in range(0, self.num_agents) if 1 in self.connectivity_matrix[index, :]]
            sender_index = random.sample(valid_senders, k=1)[0]  # sample returns a list
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            # getting ids of possible receivers
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index != sender_index)]
            # randomly pick one of the possible receivers
            receiver_index = sender_phonebook[random.randint(0, len(sender_phonebook)-1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)

    def output_measures(self):
        stats = self.simulations_stats()
        results = pd.DataFrame({"#agents": self.num_agents}, index=[0])
        results = results.join(pd.DataFrame({"#experts": stats[0]}, index=[0]))
        results = results.join(pd.DataFrame({"#neutrals": stats[2]}, index=[0]))
        results = results.join(pd.DataFrame({"#liars": stats[2]}, index=[0]))
        results = results.join(pd.DataFrame({"#initial_connections": self.num_connections}, index=[0]))
        results = results.join(pd.DataFrame({"#news": self.num_news}, index=[0]))
        # if we change stop condition this needs to change:
        results = results.join(pd.DataFrame({"#step": self.num_steps}, index=[0]))
        return results

    # initiates the simulation
    def run_simulation(self):
        print(">> Initial configurations:")
        self.simulations_stats()
        print("<< Beginning simulation >>")
        for step in tqdm(range(self.num_steps)):
            self.run_communication_protocol()
        print("<< END OF SIMULATION >>")
        self.simulations_stats()
        print(self.output_measures())