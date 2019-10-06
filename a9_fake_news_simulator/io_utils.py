import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, './saved_experiments/')


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
def load_experiment_settings(experiment='default'):
    # initialize parameters object
    params = dict()
    # read parameters from the text file
    with open(filename+experiment+'.txt') as exp:
        for line in exp:
            (key, val) = line.split()
            params[key] = val
    # cast values to appropriate types
    params = cast_param_values(params)
    return params


if __name__ == '__main__':
    load_experiment_settings('default')
