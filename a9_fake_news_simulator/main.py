import sys
import pandas as pd
from cmd import Cmd

# User defined Imports ugly python import syntax >:(
sys.path.append('./')
import environment
import io_utils

# load default parameters from file
args = io_utils.load_experiment_settings()


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
    conversation_protocol: 'discussion' \n
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
            if inp > args['n_connections']:
                print("Number of agents must be at most the number of connections so that each agent has at least "
                      "one incoming connection")
            elif inp > 0:
                args['n_agents'] = inp
                print("Setting number of agents to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_liars(self, inp):
        '''Change the number of liars. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > args['n_agents'] - args['n_experts'] or inp > args['n_agents']:
                print("Number of liars cannot be higher than the number of agents")
            elif inp > 0:
                args['n_liars'] = inp
                print("Setting number of liars to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_experts(self, inp):
        '''Change the number of experts. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > args['n_agents'] - args['n_liars'] or inp > args['n_agents']:
                print("Number of experts cannot be higher than the number of agents")
            elif inp > 0:
                args['n_experts'] = inp
                print("Setting number of experts to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_connections(self, inp):
        '''Change the number of connections. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp < args['n_agents']:
                print("Number of connections must be at least equal to number of agents so that each agent can have "
                      "one ingoing connection")
            elif inp > 0:
                args['n_connections'] = inp
                print("Setting number of connections to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_n_news(self, inp):
        '''Change the number of news. Must be an integer larger than 0'''
        try:
            inp = int(inp)
            if inp > 0:
                args['n_news'] = inp
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
                args['n_steps'] = inp
                print("Setting number of steps to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger than 0")

    def do_show_values(self, inp):
        '''Shows the current value of each parameter'''
        text = """
           The current parameter values are: \n
           n_agents: {0} 
           n_liars: {1}
           n_experts: {2} 
           n_connections: {3}
           cluster_distance: {4}
           n_news: {5}
           n_steps: {6} 
           communication_protocol: {7}
           conversation_protocol: {8}
           """
        print(text.format(args['n_agents'],
                      args['n_liars'],
                      args['n_experts'],
                      args['n_connections'],
                      args['cluster_distance'],
                      args['n_news'],
                      args['n_steps'],
                      args['communication_protocol'],
                      args['conversation_protocol']))

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
        if inp != "random" and inp != "SYO" and inp != "CO":
            print("You can only pick from the following options:  ['random', 'SYO', 'CO'] ")
        else:
            args['communication_protocol'] = inp
            print("Setting communication_protocol to '{}'".format(inp))

    def do_conversation_protocol(self, inp):
        '''The protocol that determines how a call changes the opinion of an agent.
        discussion: the call causes a discussion that has a winner. The loser of the discussion then takes on
                            the opinion of the winner with the probability 1-scepticism.
        majority_opinion: The receiver of the call remembers the opinion of the caller and then forms their opinion based
                          on what the majority of callers thinks. If a new opinion leads to a tie in opinion formation, the
                          old opinion is kept with the probability of the skepticism value.'''
        if inp != "discussion" and inp != "majority_opinion" and inp != "simple":
            print("You can only pick from the following options: ['discussion', 'majority_opinion', 'simple'] ")
        else:
            args['conversation_protocol'] = inp
            print("Setting conversation_protocol to '{}'".format(inp))

    def do_cluster_distance(self, inp):
        '''The clustering method assumes that actors are located in physical space and are embedded in 
        a social network structure that is affected by the spatial distances between them. 
        Each agent randomly got assigned a position on a 2d plane. 
        By random an agent is selected to pick an agent to connect to. 
        The connections are one-way directional from the first agent to the second. 
        The chance of a connection to the second agent, is given by: 
        exp( - 1 * cluster_distance * distance(sender, receiver))
        
		Where y is a parameter determining the slope of the chance falloff per distance, 
		and thus by consequence determining the size of the clusters. 
		When clustering_distance = 0, the network has a random structure that is not associated with 
		spatial distances between the actors and that does not show any clustering. 
		Increasing clustering_distance reduces the average distance that ties cover.'''
        try:
            inp = int(inp)
            if inp >= 0:
                args['cluster_distance'] = inp
                print("Setting cluster distance to '{}'".format(inp))
            else:
                raise ValueError
        except:
            print("Wrong input type, please enter an integer larger or equal to 0")

    def do_load_experiment(self, inp):
        if io_utils.experiment_exists(inp):
            global args  # explicitly telling python to change the outer scope args variable
            args = io_utils.load_experiment_settings(inp)
            print("Loaded experiment {0}".format(inp))
            print("Loaded parameters: {0}".format(args))

        else:
            print("Given experiment name does not exist. Check the file name and try again (not '.txt' is required)")

    def default(self, inp):
        if inp == 'x' or inp == 'q':
            return self.do_exit(inp)
        if inp == 'c' or inp == 'start':
            # initialize dataframe to keep the results of each run
            run_results_df = pd.DataFrame()
            for run in range(1, args['runs']+1):
                print("-Run {0}/{1}".format(run, args['runs']))
                network = environment.Environment(args['n_agents'], args['n_liars'], args['n_experts'],
                                                  args['n_connections'], args['cluster_distance'], args['n_news'], args['n_steps'],
                                                  args['communication_protocol'], args['conversation_protocol'])
                # combine run results with existing ones
                run_results_df = pd.concat([run_results_df, network.run_simulation()])
            # export results dataframe
            io_utils.export_results(run_results_df)
        if inp == 'show_values':
            self.do_show_values()
        if inp == 'show_description':
            self.do_show_description()
        if inp == 'run_stepwise':
            self.run_stepwise()

    def run_stepwise(self):
        network = environment.Environment(args['n_agents'], args['n_liars'], args['n_experts'],
                                          args['n_connections'], args['cluster_distance'], args['n_news'],
                                          args['n_steps'],
                                          args['communication_protocol'], args['conversation_protocol'])
        # export results dataframe
        io_utils.export_results(network.run_simulation(stepwise=True))


if __name__ == "__main__":
    main()
