import os

RELATIVE_PATH = os.path.dirname(__file__)
EXPERIMENTS_PATH = os.path.join(RELATIVE_PATH, './saved_experiments/')
RESULTS_PATH = os.path.join(RELATIVE_PATH, './results/')


# helper function checks existence of given experiment name
def experiment_exists(experiment_name):
    return os.path.isfile(EXPERIMENTS_PATH + experiment_name + '.txt')


# casts parameter values to the appropriate type
def cast_param_values(params):
    params['n_agents'] = int(params['n_agents'])
    params['n_liars'] = int(params['n_liars'])
    params['n_experts'] = int(params['n_experts'])
    params['n_connections'] = int(params['n_connections'])
    params['cluster_distance'] = int(params['cluster_distance'])
    params['n_news'] = int(params['n_news'])
    params['n_steps'] = int(params['n_steps'])
    params['runs'] = int(params['runs'])
    return params


# loads parameters from given file
def load_experiment_settings(experiment_name='default'):
    # initialize parameters object
    params = dict()
    # read parameters from the text file
    with open(EXPERIMENTS_PATH + experiment_name + '.txt') as exp:
        for line in exp:
            (key, val) = line.split()
            params[key] = val
    # cast values to appropriate types
    params = cast_param_values(params)
    return params


# exports results' dataframe to specific directory
def export_results(results_df):
    # create directory if it's not present
    if not os.path.isdir(RESULTS_PATH):
        os.mkdir(RESULTS_PATH)
    # calculate file number
    n = sum(1 for f in os.listdir(RESULTS_PATH) if os.path.isfile(os.path.join(RESULTS_PATH, f)))
    # export file
    results_df.to_csv('{0}sim_runs_{1}.csv'.format(RESULTS_PATH, n+1))
    print(">> Results file was exported in directory: {0}".format(RESULTS_PATH))

if __name__ == '__main__':
    load_experiment_settings('default')
