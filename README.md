Density - Destiny
# you must have access and a path to a FIRE galaxy in order for scripts to run 

The workflow of generating a Density-Destiny (DD) diagram is broken into two parts 
1) Data generation
2) Diagram generation

Data generation
------------------------------------------------------------------------------------
Decide what snapshots you want to track gas over and set up the script Submit_No_Loops_working_testing.py accordingly
edit lines 23, 24, and 25 to reflect the job name and .out and .error file names
edit line 29 to adjust runtime as needed to allow processing over all the snapshots you are looking to track over.
edit line 42 to reflect the script you want to run (ex. for all gas the script is No_Loops_working_testing_extra_outputs.py)
example line 42: python ../No_Loops_working_testing_scripts/No_Loops_working_testing_extra_outputs.py 258 275
this runs No_Loops_working_testing_extra_outputs.py with python and it tracks gas over snapshots 258 to 275

when this finishes running there will be 3 output files: one called destined, one called dense, and one called diffuse
if you want to track over more snapshots you will need to adjust the "extra inputs" file directly (tell it to take in the data from the most recent run)
I typically run data in batches of 25 snapshots because if you try to run 50+ in a run, you get a memory error.
For example, running from a redshift of 0.5 looked like:
258 -> 275 run with No_Loops_working_testing_extra_outputs.py 258 275
then for 275 -> 300 No_Loops_working_testing_extra_inputs.py 275 300
repeat No_Loops_working_testing_extra_outputs.py in increments of 25 until present day (or other tracking end point)

Diagram Generation
-----------------------------------------------------------------------------------
Use your most recent data output files with the density_destiny.ipynb jupyter notebook to generate the diagram. 
You will have to update the jupyter notebook to tell the program to load in your most recent data files. 
For example, in the run from redshift 0.5 to 0 (snapshots 258 -> 500) the final files needed are:
diffuse475_501.txt dense475_501.txt
Make sure the 5th cell in the jupyter notebook points to your latest run files.
After loading those in, simply run all the cells and the last one will be the DD diagram
