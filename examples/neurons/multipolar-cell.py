#!/usr/bin/env python
# -*- coding:utf-8 -*-

import dense as ds
import numpy as np
import os


'''
Main parameters
'''

S = 0.901
E = 0.3
gc_model = "run_tumble_critical"
num_neurons = 1
num_omp     = 1

neuron_params = {
    "filopodia_min_number": 30,
    "sensing_angle": 0.1495,
    "dendrite_diameter": 2.,
    "axon_diameter": 3.5,
    "position": np.array([(0., 0.)]),
    "gc_split_angle_mean": 30.,
}

dend_params = {
    "growth_cone_model": gc_model,
    "use_van_pelt": False,

    "persistence_length": 150.0,
    "thinning_ratio": 1./150.,

    # Cr model
    "res_retraction_factor": 0.005,
    "res_elongation_factor": 0.005,
    "res_retraction_threshold": 0.01,
    "res_elongation_threshold": 0.3,
    "res_leakage": 10.0,
    "res_neurite_generated": 2500.,
    "res_correlation": 0.2,
    "res_variance": 0.01,
    "res_use_ratio": 0.16,
    # "res_weight": 0.0,

    # Best model
    "gc_split_angle_mean": 1.,
    "B": 3.,
    "E": 0.,
    "S": 1.,
    "T": 5000.,
}

axon_params = {
    "growth_cone_model": gc_model,
    "use_van_pelt": False,
    "use_flpl_branching": False,

    "filopodia_wall_affinity": 2.,
    "filopodia_finger_length": 50.0,
    "thinning_ratio": 1./300.,

    "persistence_length": 250.0,

    # Cr model
    "res_retraction_factor": 0.0010,
    "res_elongation_factor": 0.01,
    # "res_weight": 0.0,
    "res_retraction_threshold": 0.10,
    "res_elongation_threshold": 0.3,
    # "res_split_th": 0.80,
    "res_neurite_generated": 2500.,
    "res_neurite_delivery_tau": 50.,
    "res_correlation": 0.4,
    "res_variance": 0.04,
    "res_use_ratio": 0.1,

    # Best model
    "gc_split_angle_mean": 1.2,
    "B": 9.,
    "E": 0.,
    "S": 1.,
    "T": 5000.,
}


'''
Growth
'''

kernel = {
    "resolution": 50.,
    "seeds": [17],
    "environment_required": False,
    "num_local_threads": num_omp,
}

ds.get_kernel_status(kernel)


# create neurons

n = ds.create_neurons(n=num_neurons, gc_model="run_tumble", params=neuron_params,
                     axon_params=axon_params, dendrites_params=dend_params,
                     #~ num_neurites=6)
                     num_neurites=1)

rec = ds.create_recorders(n, ["angle", "length"], levels="growth_cone")

# Turn branching on

#~ vp_branching = {'use_van_pelt': True}
resource_branching = {'res_branching_threshold': 80., 'res_branching_proba': 0.0005}
d_rsrc_branching = {'res_branching_threshold': 60., 'res_branching_proba': 0.0003}

#~ ds.set_object_properties(n, params=vp_branching)
#~ ds.set_object_properties(n, params=resource_branching)
ds.set_object_properties(n, axon_params=resource_branching, dendrites_params=d_rsrc_branching)

for i in range(10):
    ds.simulate(2000)
    ds.plot.plot_recording(rec, show=False)
    ds.plot.plot_neurons(show=True)


lb = {
    'res_branching_threshold': np.inf, "use_flpl_branching": True,
    "flpl_branching_rate": 0.0003, 
    "lateral_branching_angle_mean": 50.
}

lb_axon = lb.copy()
lb_axon["flpl_branching_rate"] = 0.0008

ds.set_object_properties(n, axon_params=lb_axon, dendrites_params=lb)

ds.simulate(50000)
ds.plot.plot_neurons(show=True)


end_branching = {"res_branching_threshold": 500., 'res_branching_proba': 0.0005}
ds.set_object_properties(n, axon_params=end_branching, dendrites_params=end_branching)

ds.simulate(100000)

ds.plot.plot_neurons(show=True)

ds.save_to_swc("chandelier-cell.swc", gid=n, resolution=50)

import neurom as nm
from neurom import viewer
nrn = nm.load_neuron("chandelier-cell.swc")

fig, _ = viewer.draw(nrn)

for ax in fig.axes:
    ax.set_title("")


tree = n[0].axon.get_tree()

import matplotlib.pyplot as plt
plt.axis('off')
fig.suptitle("")
plt.tight_layout()
plt.show()
tree.show_dendrogram()
