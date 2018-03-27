
#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import shutil
import time

import numpy as np
import matplotlib.pyplot as plt

import nngt

import NetGrowth as ng


def CleanFolder(tmp_dir, make=True):
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    if make:
        os.mkdir(tmp_dir)
    return tmp_dir


current_dir = os.path.abspath(os.path.dirname(__file__))
main_dir = current_dir[:current_dir.rfind("/")]


'''
Main parameters
'''

soma_radius = 10.
use_uniform_branching = False
use_vp = False
use_run_tumble = False

gc_model = 'persistent_random_walk'

neuron_params = {
}

'''
Simulation
'''


def step(n, loop_n, plot=True):
    ng.Simulate(n)
    if plot:
        ng.PlotNeuron(show_nodes=True, show=True)


if __name__ == '__main__':
    #~ kernel={"seeds":[33, 64, 84, 65],
            #~ "num_local_threads":4,
            #~ "resolution": 30.}
    kernel = {"seeds": [33, 64, 84, 65, 68, 23],
              "num_local_threads": 6,
              "resolution": 10.}
    kernel["environment_required"] = True

    culture_file = current_dir + "/diode.svg"
    ng.SetKernelStatus(kernel, simulation_ID="ID_1")
    gids, culture = None, None
    culture = ng.SetEnvironment(culture_file, min_x=0, max_x=1800)
    # generate the neurons inside the left chamber
    pos_left = culture.seed_neurons(
        neurons=200, soma_radius=soma_radius)
    pos_right = culture.seed_neurons(
        neurons=200, soma_radius=soma_radius)
    neuron_params['position'] = np.concatenate((pos_right, pos_left))

    print("Creating neurons")
    gids = ng.CreateNeurons(n=400, growth_cone_model="persistent_rw_critical",
                            culture=culture,
                            params=neuron_params,
                            num_neurites=4)

    start = time.time()
    step(35, 0, False)

    fig, ax = plt.subplots()
    duration = time.time() - start
    ng.plot.PlotNeuron(gid=range(200), culture=culture, soma_alpha=0.8,
                       axon_color='g', gc_color="r", axis=ax, show=False)
    ng.plot.PlotNeuron(gid=range(200, 400), show_culture=False, axis=ax,
                       soma_alpha=0.8, axon_color='darkorange', gc_color="r",
                       show=True)
    ng.plot.PlotNeuron(gid=range(200, 400), show_culture=False, axis=ax,
                       soma_alpha=0.8, axon_color='yellow', gc_color="r",
                       show=True)
    plt.show(block=True)
    print("SIMULATION ENDED")
    ng.ResetKernel()

    # save

    #~ kernel={"seeds":[33, 64, 84, 65],
            #~ "num_local_threads":4,
            #~ "resolution": 30.}
    kernel = {"seeds": [33, 64, 84, 65, 68, 23],
              "num_local_threads": 6,
              "resolution": 10.}
    kernel["environment_required"] = True

    culture_file = current_dir + "/diode_2.svg"
    ng.SetKernelStatus(kernel, simulation_ID="ID_2")
    gids, culture = None, None
    culture = ng.SetEnvironment(culture_file, min_x=0, max_x=1800)
    # generate the neurons inside the left chamber
    pos_left = culture.seed_neurons(
        neurons=200, soma_radius=soma_radius)
    pos_right = culture.seed_neurons(
        neurons=200, soma_radius=soma_radius)
    neuron_params['position'] = np.concatenate((pos_right, pos_left))

    print("Creating neurons")
    gids = ng.CreateNeurons(n=400, growth_cone_model="persistent_rw_critical",
                            culture=culture,
                            params=neuron_params,
                            num_neurites=4)

    start = time.time()
    step(35, 0, False)

    fig, ax = plt.subplots()
    duration = time.time() - start
    ng.plot.PlotNeuron(gid=range(200), culture=culture, soma_alpha=0.8,
                       axon_color='g', gc_color="r", axis=ax, show=False)
    ng.plot.PlotNeuron(gid=range(200, 400), show_culture=False, axis=ax,
                       soma_alpha=0.8, axon_color='darkorange', gc_color="r",
                       show=True)
    ng.plot.PlotNeuron(gid=range(200, 400), show_culture=False, axis=ax,
                       soma_alpha=0.8, axon_color='yellow', gc_color="r",
                       show=True)
    plt.show(block=True)
    print("SIMULATION ENDED")
    # ng.ResetKernel()

    # save




















    ### Import population for network analysis
    # ng_population = ng.SimulationsFromFolder(save_path)
    # import pdb; pdb.set_trace()  # XXX BREAKPOINT
    # population = ng.SwcEnsemble.from_population(ng_population)

    # intersection = ng.IntersectionsFromEnsemble(population)
    # num_connections = np.sum([len(a) for a in intersection.values()])
    # graph = ng.CreateGraph(population, intersection)
    # #graph info
    # nngt.plot.degree_distribution(graph, ['in', 'out', 'total'])
    # nngt.plot.draw_network(graph, esize=0.1, show=True)

