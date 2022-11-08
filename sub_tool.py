"""
This file contains functions that allow to generate a minimal python program,
as well as generate a minimal bash script that sends this program to a
cluster. Combined together these two functions allow for massive submission
of simulations to the cluster. 
"""

import re
import os
import subprocess


def generate_py(parameters):
    """
    Generates a minimal program with the given set of parameters. It executes
    several realizations for a given value of the parameters. To do so this
    function contains a core program stored as a string (mx_script). The keys
    in this string which encode for parameter values are then replaced by the
    actual parameters using the input dictionary (parameters)
    """

    # Define core python program
    script_template = """
# Import basic libraries
import sys, platform, time

# Print system informations
print(platform.architecture())
print(sys.version)
print(sys.executable)
print(time.strftime("Start %H:%M:%S  %d/%m/%Y"))

# Add program path
sys.path.append('/home/sartori/Repos/my_Ising_package')

# Import our program
import ising as isn

# Loop over thermal realizations
for i in range(realizations):
    output = isn.simulate(M=size, p=targets, v2=Ebinary, v3=Ecubic,
                          method=solver) # run simulations
    isn.plot_outputs(output) # plot output
    isn.process_outouts(output) # post-process output
    print(time.strftime("Evaluate %H:%M:%S  %d/%m/%Y"))
print (time.strftime("End %H:%M:%S  %d/%m/%Y"))
"""

    # Replace keys by their actual values in parameters
    pattern = re.compile("|".join(parameters.keys()))
    script = pattern.sub(lambda m: parameters[re.escape(m.group(0))],
                         script_template)

    # Generate folder and file
    path_string = parameters['local\_path'][1:-1]
    if not os.path.exists(path_string):
        os.makedirs(path_string)
    pf = open(path_string + '/script.py', 'w')
    pf.write(script)
    pf.close()

    return 0


def generate_sh(parameters):
    """
    Generates a minimal submission bash script that submits a python program.
    To do so this function contains a core script stored as a string
    (qsub_script).
    """

    # Define the submission script (do not remove hashtags)
    sbatch_script = \
"""#!/bin/bash
# Specify output file
#SBATCH --output=job_path/job_%j.out
#SBATCH --error=job_path/job_%j.err
#SBATCH --time=00:30:00
# Run the corresponding script
/home/sartori/anaconda2_linux/bin/python2.7 -u job_path/script.py
""".replace('job_path', parameters['local\_path'][1:-1])

    # Generate submission file
    path_string = parameters['local\_path'][1:-1]
    file_name = 'sbatch_script.sh'
    pf = open(path_string + '/sbatch_script.sh', 'w')
    pf.write(sbatch_script)
    pf.close()

    return 0


def submit_to_cluster(parameters, job_dict):
    """
    ASD
    """
    # Extract path string
    local_path_string = parameters['local\_path'][1:-1]

    # run sbatch on shell script
    sb_command = 'sbatch ' + local_path_string + "/sbatch_script.sh"
    sqo, msg = 1, 1  # commands.getstatusoutput(sb_command)

    # If no submission errors, append job
    if not sqo:
        job_dict[msg[20:]] = parameters['extension']
        print(msg)
    # If failed submission, append to dictionary
    if sqo:
        print('Submission failed for ' + local_path_string)
        parameters.setdefault('failed', []).append(local_path_string)

    return 0
