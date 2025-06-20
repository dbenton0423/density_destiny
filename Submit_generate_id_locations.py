#!/bin/bash
#----------------------------------------------------
# Sample Slurm job script
#   for TACC Stampede3 SKX nodes
#
#   *** Serial Job on SKX Normal Queue ***
# 
# Last revised: 20 Oct 2017
#
# Notes:
#
#   -- Copy/edit this script as desired.  Launch by executing
#      "sbatch skx.serial.slurm" on a Stampede3 login node.
#
#   -- Serial codes run on a single node (upper case N = 1).
#        A serial code ignores the value of lower case n,
#        but slurm needs a plausible value to schedule the job.
#
#   -- For a good way to run multiple serial executables at the
#        same time, execute "module load launcher" followed
#        by "module help launcher"

#SBATCH -J generate_id_locations_part3         # Job name
#SBATCH -o generate_id_locations_part3.out%j     # Name of stdout output file
#SBATCH -e generate_id_locations_part3.error%j     # Name of stderr error file
#SBATCH -p skx                  # Queue (partition) name
#SBATCH -N 1                    # Total # of nodes (must be 1 for serial)
#SBATCH -n 1                    # Total # of mpi tasks (should be 1 for serial)
#SBATCH -t 48:00:00              # Run time (hh:mm:ss)
#SBATCH --mail-user=dbenton@ucmerced.edu #CHANGE THIS TO YOUR EMAIL ADDRESS
#SBATCH --mail-type=all         # Send email at begin and end of job
#SBATCH -A TG-PHY240075         # Allocation (req'd if you have more than 1)

# Other commands must follow all #SBATCH directives...

#module list
#pwd
#date #tells you the time your code started

# Launch serial code...
source /home1/08006/dbenton/.bashrc 
python generate_id_locations_part3.py

#date
# ---------------------------------------------------
