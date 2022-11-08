"""
This is an example slurm submission script. It submits a series of jobs to
a cluster. To do so it uses accessory submission tools. For each submission
it creates a dedicated folder with the minimal python program that was
submitted, the submission bash-script used, the parameters pkl and a submission
report.
"""

import sub_tool as sub
import pickle
import numpy as np
import time

# Assign default parameters
job_dict = {}
param = {}
param['Ebinary'] = "0.5"
param['Ecubic'] = "12.0"
param['solver'] = "'newton'"
param['solver\_tolerance'] = "0.001"
param['initial\_overlap'] = "0.01"
param['size'] = "64"
param['targets'] = "3"
param['realizations'] = "1"

# Name the simulation path
sim_path = "./tmp/ising/" + \
           'ising_scale_test' + time.strftime("_%m_%d_%H_%M/")

# Define a range of sizes and replicas
range_sizes = [16, 32, 64, 128, 256, 512, 1024, 2048]
range_replicas = range(0, 10)

# Run over parameter set constructing and submitting programs
for M in range_sizes:
    # Define a range of patterns
    range_pat = np.array(M * np.linspace(0.01, 0.5, 21), dtype='int32')
    for p in range_pat:
        for r in range_replicas:
            # Assign parameters
            param['size'] = str(M)
            param['targets'] = str(p)
            param['species'] = str(M)
            param['extension'] = 'M' + str(M) + 'p' + str(p) + 'r' + str(r)
            param['local\_path'] = "'" + sim_path + param['extension'] + "'"

            # Generate program and submission files, and submit jobs
            sub.generate_py(param)
            sub.generate_sh(param)
            sub.submit_to_cluster(param, job_dict)

#   Save parameters
with open(sim_path + "parameter.pkl", "wb") as f:
    pickle.dump(param, f)
# Save association of job names and parameters
with open(sim_path + "job_dict.pkl", "wb") as f:
    pickle.dump(job_dict, f)
