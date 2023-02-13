import argparse
import yaml

import numpy as np

from model import CompartmentModel

from model import AerosolSourceSimulation

from utils import plot_results

from matplotlib import pyplot as plt 

def get_init_vals(Cp, Cs):
    vals = [Cp]
    for val in Cs:
        vals.append(val)
    return vals


if __name__ == '__main__':
    config_path = 'config.yaml'
    with(open(config_path)) as conf_file:
        config = yaml.safe_load(conf_file)

    arg_parser = argparse.ArgumentParser('Compartment Model Simulation')

    # arg_parser.add_argument('--init_Cp', )

    init_vals = get_init_vals(**config['init_vals']) 

    ## modifications
    ach = 1 # air change per hour
    config['model_params']['Q'] = ach* (config['model_params']['Vp'] + config['model_params']['Vs'][0] )

    cough_model = AerosolSourceSimulation('cough', np.linspace(0, 1, 240))

    y_points = [cough_model.get_rate(t) for t in  np.linspace(0, 1, 240)]
    plt.plot( np.linspace(0, 1, 240), y_points , '-', label='Count')
    plt.show()

    aerosol_gen_funcs = [AerosolSourceSimulation('cough', np.linspace(0, 1, 240)) for _ in range(3)]
    aerosol_gen_funcs.append(AerosolSourceSimulation('no_cough', np.linspace(0, 1, 240)))
    model = CompartmentModel(**config['model_params'], aerosol_mass_func=aerosol_gen_funcs)

    # model = CompartmentModel(**config['model_params'])

    model.setup_equations(init_vals=init_vals)
    print('Starting to solve ODE')
    
    # result = model.simulate(time_span= np.linspace(0, 1, 240), solver='odeint')
    # print(result)
    # result_cp = result.T[0]
    # result_cs = result.T[1]
    # plt.plot(np.linspace(0, 2, 240), result_cp, '-', label='Cp')
    # plt.plot(np.linspace(0, 2, 240), result_cs, '--', label='Cs')

    result = model.simulate(time_span= np.linspace(0, 1, 240), solver='ivp')
    print(result)

    plt.plot(result.t, result.y[0], '-', label='Cp')
    for i in range(config['model_params']['num_sub_compartment']):
        plt.plot(result.t, result.y[i+1], '--', label=f'Cs_{i+1}')
    plt.legend()
    plt.savefig("forecast_aerosol_flow")
    plt.show()
