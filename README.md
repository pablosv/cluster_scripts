# cluster_scripts
This is a minimal working example of how to organize submission to a slurm cluster. The file `sube_example.py` takes as input model parameters, which are stored in a dictionary. It then loops over a range of rolling parameters, e.g. system sizes in a scaling analysis, and for each set of parameters it submits a job to the cluster

Submission to the cluster is a multi-step process, first a minimal python program is generated, and stored in a folder with name related to the parameters. Second, an accompanying slurm submission script is also generated and stored in the same folder. Third, sbatch is ran on the slurm bash script, which calls the python program. Functions realizing these three steps are stored in `sub_tool.py`
