import sys
import argparse
from cmd import Cmd

# User defined Imports ugly python import syntax >:(
sys.path.append('./')
import environment

parser = argparse.ArgumentParser(description='Run a simulation')
parser.add_argument('--n_agents', type=int, default=10, help='Give the number of agents of the network.')
parser.add_argument('--n_liars', type=int, default=1, help='Give the number of liars of the network.')
parser.add_argument('--n_experts', type=int, default=1, help='Give the number of experts of the network.')
parser.add_argument('--n_connections', type=int, default=10, help='Give the number of connections in the network.')
parser.add_argument('--cluster_distance', type=int, default=0, help='Give the amount of clustering in the network.')
parser.add_argument('--n_news', type=int, default=1, help='Give the number of news in the network.')
parser.add_argument('--n_steps', type=int, default=50, help='Give the number of steps of the simulation.')
parser.add_argument('--communication_protocol', type=str, default="random",
                    help='Determines the way the agents choose whom to call. Current options: ["random"].')
parser.add_argument('--conversation_protocol', type=str, default="battle_discussion",
                    help='Determines the way a call is resolved. Current options: ["battle_discussion", "majority_opinion"].')

args = parser.parse_args()


def main():
    MyPrompt().cmdloop()


class MyPrompt(Cmd):
    prompt = 'fake_news> '
    intro = """
    Welcome! The default parameter values are: \n
    n_agents: 10 
    n_liars: 1 
    n_experts: 1  
    n_connections: 10 
    cluster_distance: 0
    n_news: 1 
    n_steps: 50 
    communication_protocol: 'random'
    conversation_protocol: 'battle_discussion' \n
    If you want to start the simulation with these values enter 'start'. 
    Otherwise change values by entering '{parameter} {value}' and then enter 'start'.
    Enter '?' for an overview over all commands.
    """

    def do_exit(self, inp):
        '''exit the application.'''
        print("Bye")
        return True

    def do_n_agents(self, inp):
        '''Change the number of agents. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_agents = inp
                print("Setting number of agents to '{}'".format(inp))
            if inp > args.n_connections:
                print("Number of agents must be at most the number of connections so that each agent has at least "
                      "one incoming connection")
                raise ValueError
            # todo: raise different error
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_liars(self, inp):
        '''Change the number of liars. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_liars = inp
                print("Setting number of liars to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_experts(self, inp):
        '''Change the number of experts. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_experts = inp
                print("Setting number of experts to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_connections(self, inp):
        '''Change the number of connections. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_connections = inp
                print("Setting number of connections to '{}'".format(inp))
            if inp < args.n_agents:
                print("Number of connections must be at least equal to number of agents so that each agent can have "
                      "one ingoing connection")
                raise ValueError
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_news(self, inp):
        '''Change the number of news. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_news = inp
                print("Setting number of news to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_steps(self, inp):
        '''Change the number of steps. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args.n_steps = inp
                print("Setting number of steps to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_show_values(self, inp):
        '''Shows the current value of each parameter'''
        text = """
           The current parameter values are: \n
           n_agents: %s 
           n_liars: %s 
           n_experts: %s 
           n_connections: %s
           cluster_distance: %s
           n_news: %s
           n_steps: %s 
           communication_protocol: %s
           conversation_protocol: %s
           """
        print(text % (args.n_agents,
                      args.n_liars,
                      args.n_experts,
                      args.n_connections,
                      args.cluster_distance,
                      args.n_news,
                      args.n_steps,
                      args.communication_protocol,
                      args.conversation_protocol))

    def do_show_description(self, inp):
        '''Shows a description of the program and how the simulation works'''
        text = """
            This is a project on the spread of fake news in a social network created in the scope of the course 
            'Design of Multi-Agent Systems'.
            Authors: Panagiotis, Anton, Manvi, Daniel
           """
        # todo: write better description
        print(text)

    def do_communication_protocol(self, inp):
        '''The protocol that determines how agent choose to call other agents.
        random: a random agent is picked from the phonebook.'''
        if inp != "random":
            print("You can only pick from the following options:  ['random'] ")
        else:
            args.communication_protocol = inp
            print("Setting communication_protocol to '{}'".format(inp))

    def do_conversation_protocol(self, inp):
        '''The protocol that determines how a call changes the opinion of an agent.
        battle_discussion: the call causes a discussion that has a winner. The loser of the discussion then takes on
                            the opinion of the winner with the probability 1-scepticism.
        majority_opinion: The receiver of the call remembers the opinion of the caller and then forms their opinion based
                          on what the majority of callers thinks. If a new opinion leads to a tie in opinion formation, the
                          old opinion is kept with the probability of the skepticism value.'''
        if inp != "battle_discussion" and inp != "majority_opinion":
            print("You can only pick from the following options: ['battle_discussion', 'majority_opinion'] ")
        else:
            args.conversation_protocol = inp
            print("Setting conversation_protocol to '{}'".format(inp))

    def do_cluster_distance(self, inp):
        ''' Daniel, please add explanatoin here'''
        # todo: add explanation
        try:
            inp = int(inp)
            if inp >= 0:
                args.cluster_distance = inp
                print("Setting cluster distance to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger or equal to 0")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        if inp == 'c' or inp == 'start':
            network = environment.Environment(args.n_agents, args.n_liars, args.n_experts,
                                              args.n_connections, args.cluster_distance, args.n_news, args.n_steps,
                                              args.communication_protocol, args.conversation_protocol)
            print(network.clustering_coefficient())
            network.run_simulation()
        if inp == 'show_values':
            self.do_show_values()
        if inp == 'show_description':
            self.do_show_description()


if __name__ == "__main__":
    main()
