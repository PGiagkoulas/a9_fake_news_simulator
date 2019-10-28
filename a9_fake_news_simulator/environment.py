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
    num_connections = None  # the connectivity of the network
    num_news = None  # number of different news propagating in the network (=1 for now)
    num_steps = None  # how long the simulation will run
    agent_list = None  # list of all agents
    connectivity_matrix = None  # keeps all the connections between agents in the network (row [HAS_CONNECTION_WITH] column)
    communication_protocol = None  # determines how agents choose whom to call
    conversation_protocol = None  # determines how a conversation takes place and how agents change their opinion
    connectivity = None  # determines the initial architecture of the network
    n_isolates = None  # number of isolated agents in the network, after initialization

    # initializer
    def __init__(self,
                 num_agents,
                 num_liars,
                 num_experts,
                 num_connections,
                 cluster_distance,
                 num_news,
                 num_steps,
                 connectivity_type,
                 communication_protocol="random",
                 conversation_protocol="discussion"):
        self.num_agents = num_agents
        self.num_liars = num_liars
        self.num_experts = num_experts
        self.num_connections = num_connections
        self.cluster_distance = cluster_distance
        self.connectivity = connectivity_type
        self.num_news = num_news
        self.num_steps = num_steps
        self.agent_list = self._generate_agents()
        self.connectivity_matrix = self._initialize_connectivity_matrix()
        # detect isolated agents and make them convinced
        self.n_isolates = self.convince_isolates()
        self.communication_protocol = communication_protocol
        self.conversation_protocol = conversation_protocol

    # generates a list of the network's agents (private)
    def _generate_agents(self):
        list_of_agents = []
        for number in range(self.num_agents):
            # agents are initially generated neutral and
            # their scepticism follows a normal distribution around the average scepticism level
            list_of_agents.append(agent.Agent(opinion=0,
                                              scepticism=random.gauss(0.5, 0.1),
                                              num_agents=self.num_agents,
                                              id=number,
                                              persuasiveness=random.gauss(0.5, 0.1)))

        # assign opinions to agents
        agent_indexes = random.sample(range(len(list_of_agents)), k=self.num_liars + self.num_experts)
        # declare liars & experts
        # they will not change their opinion (scepticism = 1)
        for a in agent_indexes[:self.num_liars]:
            list_of_agents[a].opinion = -1
            list_of_agents[a].scepticism = 1
            list_of_agents[a].convinced = True
        for a in agent_indexes[self.num_liars:]:
            list_of_agents[a].opinion = 1
            list_of_agents[a].scepticism = 1
            list_of_agents[a].expert = True
            list_of_agents[a].convinced = True
            list_of_agents[a].persuasiveness = 1
        return list_of_agents

    # initialize connectivity matrix
    def _initialize_connectivity_matrix(self):
        connectivity_matrix = np.zeros((self.num_agents, self.num_agents), dtype=int)
        if self.connectivity == "cluster" or self.connectivity == "random":
            if self.cluster_distance == 0:
                return self.init_random(connectivity_matrix)

            else:
                return self.init_cluster(connectivity_matrix)
        if self.connectivity == "sun":
            return self.init_sungraph(connectivity_matrix)
        if self.connectivity == "circle":
            return self.init_circlegraph(connectivity_matrix)

    # The different methods for connectivity
    def init_random(self, connectivity_matrix):
        for number in range(self.num_connections):
            # randomly decide connection between 2 agents
            pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # repeat until pair is not already connected
            while connectivity_matrix[pair[0], pair[1]] == 1:
                pair = np.random.randint(low=0, high=self.num_agents, size=2)
            # update matrix
            connectivity_matrix[pair[0], pair[1]] = 1
        return connectivity_matrix

    def init_cluster(self, connectivity_matrix):
        # assign for every agent a x and y position value
        list_of_xy = []
        for i in range(self.num_agents):
            list_of_xy.append((np.random.randint(low=0, high=100), np.random.randint(low=0, high=100)))

        for number in range(self.num_connections):
            pair = np.random.randint(low=0, high=self.num_agents, size=1).tolist()
            pair.append(pair[0])
            chance = [0] * self.num_agents

            # repeat until pair is not already connected
            while connectivity_matrix[pair[0]][pair[1]] == 1 or pair[0] == pair[1]:
                for connection in range(len(connectivity_matrix[pair[0]])):
                    if connectivity_matrix[pair[0]][connection] == 1:
                        chance[connection] = 0
                    else:
                        dist = self.distance(list_of_xy[pair[0]], list_of_xy[connection])
                        chance[connection] = math.exp(
                            - 1 * self.cluster_distance * dist)

                # calculation of chance of connection based on relative distance
                chance[pair[0]] = 0
                if sum(chance) == 0:  # no possible connections left
                    pair = np.random.randint(low=0, high=self.num_agents, size=1).tolist()
                    pair.append(pair[0])
                else:
                    elected = np.random.uniform(0, sum(chance))
                    compare = 0
                    # print(chance)
                    # print(sum(chance))
                    # print(elected)

                    for connection in range(len(connectivity_matrix[pair[0]])):
                        compare += chance[connection]
                        if elected <= compare:
                            pair[1] = connection
                            break

            # update matrix
            connectivity_matrix[pair[0], pair[1]] = 1

        return connectivity_matrix

    def init_sungraph(self, connectivity_matrix):
        if (self.num_agents % 2) == 1:
            print("warning uneven amount of agents for sun graph, removing 1")
            self.num_agents -= 1

        for i in range(int(self.num_agents / 2)):
            # put half of the agents into circle formation
            if i + 1 < self.num_agents / 2:
                connectivity_matrix[i][i + 1] = 1
            else:
                connectivity_matrix[i][0] = 1
            # set the other half to be connected to 1 unique node each of the circle
            connectivity_matrix[int(self.num_agents / 2 + i)][i] = 1
        return connectivity_matrix

    def init_circlegraph(self, connectivity_matrix):
        for i in range(self.num_agents):
            if i + 1 < self.num_agents:
                connectivity_matrix[i][i + 1] = 1
            else:
                connectivity_matrix[i][0] = 1
        return connectivity_matrix

    # conversation protocol
    def agent_conversation(self, agent_a, agent_b):
        # exchanging the phonebook always happens
        self.exchange_phonebooks(agent_a, agent_b)
        if self.conversation_protocol == "discussion":
            # agent_a is the sender and agent_b the receiver
            if agent_a.opinion != agent_b.opinion or (agent_a.expert or agent_b.expert):
                # determine winning opinion of the communication
                # neutral opinions do not spread, the other agent's opinion automatically wins
                if agent_a.opinion == 0 or agent_b.expert:
                    winner = 2  # opinion of agent_b is the outcome of discussion
                elif agent_b.opinion == 0 or agent_a.expert:
                    winner = 1  # opinion of agent_a is the outcome of discussion
                else:  # randomly decide winning opinion
                    winner = self.calculate_winner(agent_a.persuasiveness, agent_b.persuasiveness)
                # resolve agent acceptance
                if winner == 1:
                    agent_b.evaluate_opinion(agent_a.opinion, agent_a.expert)
                elif winner == 2:
                    agent_a.evaluate_opinion(agent_b.opinion, agent_b.expert)
            # after evaluation, the opinion bases are updated
            agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
            agent_a.opinion_base[self.agent_list.index(agent_b)] = agent_b.opinion
        elif self.conversation_protocol == "majority_opinion":
            # agent_a is the sender and agent_b the receiver
            # the opinion bases are updated
            agent_a.opinion_base[self.agent_list.index(agent_b)] = agent_b.opinion
            agent_b.opinion_base[self.agent_list.index(agent_a)] = agent_a.opinion
            # opinions are formed based on the updated opinion bases
            agent_a.form_opinion(agent_b.expert)
            agent_b.form_opinion(agent_a.expert)
        elif self.conversation_protocol == "simple":
            # the receiver simply takes on the opinion of the sender with a certain probability based on their
            # scepticism
            if agent_a.opinion != 0:
                agent_b.evaluate_opinion(agent_a.opinion, agent_a.expert)
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
        # agents get each other's contact
        self.connectivity_matrix[index_a, index_b] = 1
        self.connectivity_matrix[index_b, index_a] = 1
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
                # if the phonebook is empty nothing has changed in this time step
                return False
            # randomly pick one of the possible receivers
            receiver_index = sender_phonebook[random.randint(0, len(sender_phonebook) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
            # if something changed, it returns true. This is used for counting successful step
            return True
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
                # if there are not valid contacts, nothing changes in this time step
                return False
            receiver_index = valid_contacts[random.randint(0, len(valid_contacts) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
            # if something changed, it returns true. This is used for counting successful step
            return True
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
                # if there are not valid contacts, nothing changes in this time step
                return False
            receiver_index = valid_contacts[random.randint(0, len(valid_contacts) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
            # if something changed, it returns true. This is used for counting successful step
            return True
        elif self.communication_protocol == "LNS":
            sender_index = self.choose_random_sender()
            sender = self.agent_list[sender_index]
            # choose receiver
            # getting sender's connections
            sender_connectivity = self.connectivity_matrix[sender_index, :]
            # getting ids of possible receivers
            sender_phonebook = [index for index in range(0, self.num_agents)
                                if (sender_connectivity[index] != 0 and index != sender_index)]
            # only select those contacts that you never had a conversation with
            # or if you know that they have a neutral opinion
            valid_contacts = [contact for contact in sender_phonebook if
                              sender.opinion_base[contact] is None or sender.opinion_base[contact] == 0]
            if len(valid_contacts) == 0:
                # if there are not valid contacts, nothing changes in this time step
                return False
            receiver_index = valid_contacts[random.randint(0, len(valid_contacts) - 1)]  # randint is inclusive
            receiver = self.agent_list[receiver_index]
            self.agent_conversation(sender, receiver)
            # if something changed, it returns true. This is used for counting successful step
            return True

    def choose_random_sender(self):
        # choose agent to communicate
        valid_senders = [index for index in range(0, self.num_agents) if 1 in self.connectivity_matrix[index, :]]
        return random.sample(valid_senders, k=1)[0]  # sample returns a list

    def output_measures(self, step=None):
        stats = self.simulations_stats()
        if step:
            results = {"#agents": [self.num_agents],
                       "current step": [step],
                       "#positives": [stats[0]],
                       "#neutrals": [stats[1]],
                       "#negatives": stats[2],
                       "#isolates": self.n_isolates,
                       "#experts": self.num_experts,
                       "#liars": self.num_liars,
                       "#initial_connections": self.num_connections,
                       "#news": self.num_news,
                       "#cluster distance": self.cluster_distance,
                       "#comm_protocol": self.communication_protocol,
                       "#conv_protocol": self.conversation_protocol,
                       "#steps": self.num_steps
                       }
        else:
            results = {"#agents": [self.num_agents],
                       "#positives": [stats[0]],
                       "#neutrals": [stats[1]],
                       "#negatives": stats[2],
                       "#isolates": self.n_isolates,
                       "#experts": self.num_experts,
                       "#liars": self.num_liars,
                       "#initial_connections": self.num_connections,
                       "#news": self.num_news,
                       "#cluster distance": self.cluster_distance,
                       "#comm_protocol": self.communication_protocol,
                       "#conv_protocol": self.conversation_protocol,
                       "#steps": self.num_steps
                       }
        return pd.DataFrame(results)

    # runs the simulation
    def run_simulation(self, verbose=False, stepwise=False):
        final_step = 0
        skip_step = 10  # how often to print with step-wise
        run_results_df = pd.DataFrame()
        # to decrease the number of lines in the csvs we count only the steps in which agents actually communicated
        successful_steps = 1
        for step in tqdm(range(1, self.num_steps + 1)):
            if self.converged():
                final_step = successful_steps
                break
            if (self.communication_protocol == 'CO' or self.communication_protocol == 'LNS') and self.all_contacted():
                final_step = successful_steps
                break
            changed = self.run_communication_protocol()
            if changed:
                successful_steps += 1
                if stepwise and (step == 1 or step % skip_step == 0):
                    # only concat new line to dataframe if a conversation took place
                    run_results_df = pd.concat([run_results_df, self.output_measures(successful_steps)])
        if stepwise:
            return run_results_df
        else:
            return self.output_measures(step=final_step)

    # calculates distance
    def distance(self, xy1, xy2):
        return math.sqrt(pow((xy1[0] - xy2[0]), 2) + pow((xy1[1] - xy2[1]), 2))

    # evaluates winner of conversation
    def calculate_winner(self, persuasiveness_a, persuasiveness_b):
        # normalize the probabilities
        a = persuasiveness_a / (persuasiveness_a + persuasiveness_b)
        b = persuasiveness_b / (persuasiveness_a + persuasiveness_b)
        if random.uniform(0.0, 1.0) > a:
            return 2
        else:
            return 1

    # checks if simulation has converged (no more opinion propagation possible)
    def converged(self):
        if all([agent.convinced for agent in self.agent_list]):
            return True
        else:
            return False

    # detects all isolated agents and sets their convinced flag to 1, since they will never have an option of
    # changing opinion + returns the number of isolates in the network
    def convince_isolates(self):
        isolates = 0
        for index in range(self.num_agents):
            outgoing = self.connectivity_matrix[index, :]
            incoming = self.connectivity_matrix[:, index]
            if all([inc == 0 for inc in incoming]) and all([out == 0 for out in outgoing]):
                self.agent_list[index].convinced = 1
                isolates += 1
        return isolates

    # checks if there are still valid senders/receivers in the network
    def all_contacted(self):
        # assume all agents have been contacted
        all_contacted = True
        for agent_index, agent in enumerate(self.agent_list):
            # getting sender's connections
            agent_connectivity = self.connectivity_matrix[agent_index, :]
            # getting ids of possible receivers
            agent_phonebook = [index for index in range(0, self.num_agents)
                               if (agent_connectivity[index] != 0 and index != agent_index)]
            if self.communication_protocol == 'CO':
                valid_contacts = [contact for contact in agent_phonebook if agent.opinion_base[contact] is None]
            elif self.communication_protocol == 'LNS':
                valid_contacts = [contact for contact in agent_phonebook
                                   if agent.opinion_base[contact] is None or agent.opinion_base[contact] == 0]
            if valid_contacts:
                all_contacted = False
                return all_contacted
        return all_contacted

