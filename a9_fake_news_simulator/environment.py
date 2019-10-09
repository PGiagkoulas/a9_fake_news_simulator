import sys
import random
import numpy as np
import pandas as pd
import math
from tqdm import tqdm

sys.path.append('./')
import agent


class Environment:
    # attributes
    num_agents = None  # number of agents in the network
    num_liars = None  # number of liars (opinion = -1)
    num_experts = None  # number of liars (opinion = 1)
    num_connections = None  # the connectivity of the network TODO: change to something more elaborate
    global_clustering_coefficient = "none"  # average of 'the amount of connections of each agent divided by the amount of possible connections for each agent'
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
                 cluster_distance,
                 num_news,
                 num_steps,
                 communication_protocol="random",
                 conversation_protocol="discussion"):
        self.num_agents = num_agents
        self.num_liars = num_liars
        self.num_experts = num_experts
        self.num_connections = num_connections
        self.cluster_distance = cluster_distance
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
        total_connections = self.num_connections
        connectivity_matrix = np.zeros((self.num_agents, self.num_agents), dtype=int)
        if self.cluster_distance == 0:
            for i in range(len(connectivity_matrix)):
                # guarantee that every agent is in at least one phonebook by someone else
                neighbour = i
                while neighbour == i:
                    neighbour = np.random.randint(low=0, high=self.num_agents)
                connectivity_matrix[neighbour, i] = 1
                total_connections -= 1

            for number in range(total_connections):
                # randomly decide connection between 2 agents
                pair = np.random.randint(low=0, high=self.num_agents, size=2)
                # repeat until pair is not already connected
                while connectivity_matrix[pair[0], pair[1]] == 1:
                    pair = np.random.randint(low=0, high=self.num_agents, size=2)
                # update matrix
                connectivity_matrix[pair[0], pair[1]] = 1
            return connectivity_matrix

        else:
            # assign for every agent a x and y position value
            list_of_xy = []
            for i in range(self.num_agents):
                list_of_xy.append((np.random.randint(low=0, high=100), np.random.randint(low=0, high=100)))

            for i in range(len(connectivity_matrix)):
                # guarantee that every agent is in at least one phonebook by someone else
                neighbour = i
                while neighbour == i:
                    neighbour = np.random.randint(low=0, high=self.num_agents)
                connectivity_matrix[neighbour, i] = 1
                total_connections -= 1

            for number in range(total_connections):
                # randomly decide connection between 2 agents based on the spacial distance

                pair[0] = np.random.randint(low=0, high=self.num_agents, size=1)
                pair[1] = pair[0]
                chance = None

                # repeat until pair is not already connected
                while connectivity_matrix[pair[0], pair[1]] == 1:
                    for connection in range(len(connectivity_matrix[selected])):
                        chance[connection] = math.exp(
                            - 1 * self.cluster_distance * distance(list_of_xy[selected], list_of_xy[connection]))
                    # calculation of chance of connection based on relative distance

                    elect = np.random.randfloat(0, sum(chance))
                    compare = 0

                    for connection in range(len(connectivity_matrix[selected])):
                        compare += chance[connection]
                        if elected <= compare:
                            pair[1] = connection

                # update matrix
                connectivity_matrix[pair[0], pair[1]] = 1

            return connectivity_matrix

    # conversation protocol
    def agent_conversation(self, agent_a, agent_b):
        # exchanging the phonebook always happens
        self.exchange_phonebooks(agent_a, agent_b)
        if self.conversation_protocol == "discussion":
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
                # after evaluation, the opinion bases are updated
                agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
                agent_a.opinion_base[self.agent_list.index(agent_b)] = agent_b.opinion
        elif self.conversation_protocol == "majority_opinion":
            # agent_a is the sender and agent_b the receiver
            # neutral opinions don't spread
            if agent_a.opinion != 0:
                agent_b.form_opinion()
            # after evaluation, the opinion bases are updated
            agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
            agent_a.opinion_base[self.agent_list.index(agent_b)] = agent_b.opinion
        elif self.conversation_protocol == "simple":
            # the receiver simply takes on the opinion of the sender with a certain probability based on their
            # scepticism
            if agent_a.opinion != 0:
                agent_b.evaluate_opinion(agent_a.opinion)
            agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
            agent_a.opinion_base[self.agent_list.index(agent_b)] = agent_b.opinion

    # printing statistics/results of simulation
    def simulations_stats(self, printing=False):
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
        if printing:
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
        union_phonebook = [(connection if connection < 1 else 1) for connection in phonebook_a + phonebook_b]
        # update connectivity matrix
        self.connectivity_matrix[index_a, :] = union_phonebook
        self.connectivity_matrix[index_b, :] = union_phonebook
        # make certain no connection is made from the agents to themselves
        self.connectivity_matrix[index_a, index_a] = 0
        self.connectivity_matrix[index_b, index_b] = 0

    def run_communication_protocol(self):
        # todo: refactor this monster of a method. so much redundancy, it really smells terrible
        if self.communication_protocol == "random":
            sender_index = self.choose_random_sender()
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            # getting ids of possible receivers
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index != sender_index)]
            if not sender_phonebook:
                # stop if the phonebook is empty
                return
            # randomly pick one of the possible receivers
            receiver_index = sender_phonebook[random.randint(0, len(sender_phonebook) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
        elif self.communication_protocol == "SYO":
            # in this protocol makes agents try to convince everyone they know of their own opinion
            sender_index = self.choose_random_sender()
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            # getting ids of possible receivers
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index != sender_index)]
            # only select those contacts from which you know, that they don't already share your opinion
            valid_contacts = [contact for contact in sender_phonebook if
                              sender.opinion_base[contact] != sender.opinion]
            if not valid_contacts:
                return
            receiver_index = valid_contacts[random.randint(0, len(valid_contacts) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
        elif self.communication_protocol == "CO":
            # Communicate once is the better name for CMO
            # in this protocol makes agents try to convince everyone they know of their own opinion
            sender_index = self.choose_random_sender()
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            # getting ids of possible receivers
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index != sender_index)]
            # only select those contacts that you never had a conversation with
            # after every conversation the opinion base is updated so can just check against None
            valid_contacts = [contact for contact in sender_phonebook if
                              sender.opinion_base[contact] is None]
            if not valid_contacts:
                return
            receiver_index = valid_contacts[random.randint(0, len(valid_contacts) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)

    def choose_random_sender(self):
        # choose agent to communicate
        valid_senders = [index for index in range(0, self.num_agents) if 1 in self.connectivity_matrix[index, :]]
        return random.sample(valid_senders, k=1)[0]  # sample returns a list

    def output_measures(self, step=None):
        stats = self.simulations_stats()
        results = pd.DataFrame({"#agents": self.num_agents}, index=[0])
        if step:
            results = results.join(pd.DataFrame({"current step": step}, index=[0]))
        results = results.join(pd.DataFrame({"#positives": stats[0]}, index=[0]))
        results = results.join(pd.DataFrame({"#neutrals": stats[1]}, index=[0]))
        results = results.join(pd.DataFrame({"#negatives": stats[2]}, index=[0]))
        results = results.join(pd.DataFrame({"#experts": self.num_experts}, index=[0]))
        results = results.join(pd.DataFrame({"#liars": self.num_liars}, index=[0]))
        results = results.join(pd.DataFrame({"#initial_connections": self.num_connections}, index=[0]))
        results = results.join(pd.DataFrame({"#news": self.num_news}, index=[0]))
        results = results.join(pd.DataFrame({"#cluster distance": self.cluster_distance}, index=[0]))
        results = results.join(pd.DataFrame({"#comm_protocol": self.communication_protocol}, index=[0]))
        results = results.join(pd.DataFrame({"#conv_protocol": self.conversation_protocol}, index=[0]))

        # if we change stop condition this needs to change:
        results = results.join(pd.DataFrame({"#steps": self.num_steps}, index=[0]))
        return results

    # runs the simulation
    def run_simulation(self, verbose=False):
        if verbose:  # prints only if explicitly stated
            print(">> Initial configurations:")
            self.simulations_stats()
            print("<< Beginning simulation >>")
        for step in tqdm(range(self.num_steps)):
            self.run_communication_protocol()
            # print(self.output_measures(step))
        if verbose:  # prints only if explicitly stated
            print("<< END OF SIMULATION >>")
            self.simulations_stats(printing=True)
        return self.output_measures()

    # calculates distance
    def distance(self, xy1, xy2):
        return math.sqrt(pow((xy1[0] - xy2[0]), 2) + pow((xy1[1] - xy2[1]), 2))

    # calculate local clustering coefficiant
    def clustering_coefficient(self):
        temp_neighbours = []
        neighbour_connections = 0
        total_possible_connections = 0
        for i in range(self.num_agents):
            for j in range(len(self.connectivity_matrix[i])):
                if self.connectivity_matrix[i][j] == 1:
                    temp_neighbours.append(self.connectivity_matrix[i][j])
            for n in temp_neighbours:
                # for each neighbour, check whether their neighbours are also connected (receivers) of the original agent
                for nj in range(len(self.connectivity_matrix[n])):
                    if self.connectivity_matrix[i][nj] == 1:
                        neighbour_connections += 1
                total_possible_connections += len(temp_neighbours) - 1
        return neighbour_connections / total_possible_connections / self.num_agents
