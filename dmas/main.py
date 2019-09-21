import sys
import argparse
# User defined Imports ugly python import syntax >:(
sys.path.append('./')
import environment

parser = argparse.ArgumentParser(description='Run a simulation')
parser.add_argument('--n_agents', type=int, default=10, help='Give the number of agents of the network.')
parser.add_argument('--n_liars', type=int, default=1, help='Give the number of liars of the network.')
parser.add_argument('--n_experts', type=int, default=1, help='Give the number of experts of the network.')
parser.add_argument('--n_connections', type=int, default=3, help='Give the number of connections in the network.')
parser.add_argument('--n_news', type=int, default=1, help='Give the number of news in the network.')
parser.add_argument('--n_steps', type=int, default=50, help='Give the number of steps of the simulation.')

args = parser.parse_args()

def main():
    network = environment.Environment(args.n_agents, args.n_liars, args.n_experts,
                                      args.n_connections, args.n_news, args.n_steps)
    network.run_simulation()

if __name__ == "__main__":
    main()