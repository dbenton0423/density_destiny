### IMPORTS ###

import numpy as np 
import matplotlib.pyplot as plt
#import pandas as pd
import gizmo_analysis as gizmo  
import utilities as ut
import time as t
import gc
import random
import statistics

import sys
sstart, send = sys.argv[1], sys.argv[2]
start = int(sstart)
end   = int(send)

outpath = '/work/08006/dbenton/stampede3/velocity/'



#############################################################################
# CONSTANTS, BINNINGS, CUTS
#############################################################################

MsunToGm = 1.99e33
KpcToCm  = 3.086e21
mp       = 1.67e-24

bin_edge = 30. # out to Rcyl = 30 kpc
bins     = np.arange(-25,25,0.1)
zmax     = 1.5  # include only gas/stars within +/- 1.5 kpc of plane of disk
age_min  = 4    # age minimum in Myr
age_max  = 6    # age maximum in Myr
den_min  = (1e-4)#/((MsunToGm/KpcToCm**3)/mp)
den_max  = (1e3)#/((MsunToGm/KpcToCm**3)/mp) #in units of n/cm^3
print(den_min)



#########################################################################################################

### LOADING AND READING IN THE SIMULATION (FIRST SNAPSHOT) ###

simname = '/scratch/04712/tg840119/m12i_m7e3_HD_fire3_fireBH_Sep052021_hr_crdiffc690_sdp1e10_gacc31_fa0.5'                                                         
simdir = '/scratch/04712/tg840119/m12i_m7e3_HD_fire3_fireBH_Sep052021_hr_crdiffc690_sdp1e10_gacc31_fa0.5'

part = gizmo.io.Read.read_snapshots(['star','gas'],'index', 258
                                    , simulation_name=simname, simulation_directory=simdir,
                                    assign_hosts_rotation=True, assign_hosts=True)



#########################################################################################################




### FEEDING DATA FROM LOADED SNAPSHOT ABOVE INTO RESPECTIVE ARRAYS ###
gas_ids = part['gas']['id']
gas_gen = part['gas']['id.generation']
gas_den = part['gas']['density']
gas_child = part['gas']['id.child']
gas_feh = part['gas'].prop('metallicity.fe')
R_0 = part['gas'].prop('host.distance.principal.cylindrical')[:,0]
#r_0 = part['gas'].prop('host.distance.principal.spherical')[:,0]
z = part['gas'].prop('host.distance.principal.cartesian')[:,2]

#Radial velocity to galactic center 
#Rotatational velocity 
#Up down velociity (z dir) (vel dotted with abs val z )

v_R     = part['gas'].prop('host.velocity.principal.cylindrical')[:,0]
v_theta = part['gas'].prop('host.velocity.principal.cylindrical')[:,1]
v_z     = part['gas'].prop('host.velocity.principal.cylindrical')[:,2]



selection = (gas_gen == 0) & (gas_child == 0) 
gas_ids_selected = gas_ids[selection]

gas_feh = gas_feh[selection]

gas_ids_selected_sorted = np.sort(gas_ids_selected)


dosort = np.argsort(gas_ids_selected)


gas_den_selected = gas_den[selection]





print(len(gas_ids_selected)) #snap 13 has 70506833 gas cells 
print(max(gas_ids_selected))

print(gas_ids_selected[0])
print(gas_den_selected[0])
print(gas_den_selected[np.where(gas_ids_selected == 0)[0]])


# In[ ]:


snapshot_number = range(start , end, 1)
ids = np.zeros([len(gas_ids_selected_sorted), (len(snapshot_number) + 1)], dtype=int)

ids[:,0] = gas_ids_selected_sorted








destined = np.loadtxt(outpath + 'destined_velocity' + str(425) + '_'+ str(450) + '.txt')

#print('########### destinies reached ##########')
#k = 0
#for i in range(len(destined)):
#    if destined[i] == 0:
#       k=k+1
#print(k)
# at the end there are 70053398 cells that reached a destiny (?) seems way too high





gas_den_ncm3_selected = gas_den_selected*((MsunToGm/KpcToCm**3)/mp)


den = np.zeros([len(gas_ids_selected_sorted), (len(snapshot_number) + 1)])

den[:,0] = gas_den_ncm3_selected[dosort]

gas_feh = gas_feh[dosort]


print(min(den[:,0]))
print(max(den[:,0]))

#print(den[158729,0])
#print(ids[158729,0])
#print(np.where(gas_ids_selected == 1005399))
#print(gas_den_selected[15246553]*((MsunToGm/KpcToCm**3)/mp))
#print(ids)
#print(np.min(den[:,0]))


# In[ ]:


#analysis of first snapshot
plt.hist(den[:,0], bins = 100 )
plt.xscale('log')


# In[3]:


is_dense = []
is_diffuse = []

inst_is_dense = []
inst_is_diffuse = []

#high_v_R_inst_is_dense = []
#high_v_R_inst_is_diffuse = []

#low_v_R_inst_is_dense = []
#low_v_R_inst_is_diffuse = []

inflow_v_z_inst_is_dense = []
inflow_v_z_inst_is_diffuse = []

outflow_v_z_inst_is_dense = []
outflow_v_z_inst_is_diffuse = []








load_outflow_v_z_dense = np.loadtxt(outpath + 'dense_outflow_v_z' + str(425) + '_'+ str(450) + '.txt')
load_outflow_v_z_diffuse = np.loadtxt(outpath + 'diffuse_outflow_v_z' + str(425) + '_'+ str(450) + '.txt')

load_inflow_v_z_dense = np.loadtxt(outpath + 'dense_inflow_v_z' + str(425) + '_'+ str(450) + '.txt')
load_inflow_v_z_diffuse = np.loadtxt(outpath + 'diffuse_inflow_v_z' + str(425) + '_'+ str(450) + '.txt')
          
load_dense_ids = np.loadtxt(outpath + 'ids/' + 'dense_ids_velocity_' + str(425) + '_' + str(450) + '.txt')
load_diffuse_ids = np.loadtxt(outpath + 'ids/' + 'diffuse_ids_velocity_' + str(425) + '_' + str(450) + '.txt')
    
    
#print('############## how many became stars ###############   ')
#print(len(load_dense))
#print('############# how many became diffuse #############')
#print(len(load_diffuse))


for i in range(len(load_outflow_v_z_dense)):
    outflow_v_z_inst_is_dense.append(load_outflow_v_z_dense[i])
                             
for i in range(len(load_inflow_v_z_dense)):
    inflow_v_z_inst_is_dense.append(load_inflow_v_z_dense[i])
        
        
for i in range(len(load_outflow_v_z_diffuse)):
    outflow_v_z_inst_is_diffuse.append(load_outflow_v_z_diffuse[i])        
        
for i in range(len(load_inflow_v_z_diffuse)):
    inflow_v_z_inst_is_diffuse.append(load_inflow_v_z_diffuse[i])
                             
for i in range(len(load_dense_ids)):
    is_dense.append(load_dense_ids[i])        
        
for i in range(len(load_diffuse_ids)):
    is_diffuse.append(load_diffuse_ids[i])
        
        
        
        
        
        
        
#destined = np.ones(len(den[:,0]), dtype = int) #all 1s to start, 
#become 0 as gas reaches a destiny





# In[ ]:
### SAVING THE INITIAL CONDITIONS TO USE IN FUTURE ###






# In[ ]:


#cell above previous version
for i in range(len(snapshot_number)):
    simname = '/scratch/04712/tg840119/m12i_m7e3_HD_fire3_fireBH_Sep052021_hr_crdiffc690_sdp1e10_gacc31_fa0.5'                                                         
    simdir = '/scratch/04712/tg840119/m12i_m7e3_HD_fire3_fireBH_Sep052021_hr_crdiffc690_sdp1e10_gacc31_fa0.5'
    part_z = gizmo.io.Read.read_snapshots(['star','gas'],'index', snapshot_number[i], simulation_name=simname, simulation_directory=simdir,
                                    assign_hosts_rotation=True, assign_hosts=True)
    print(i)
    t_t1 = t.time()
    #all quantities marked 'z' refer to a future snapshot (lower number of gas cells) (no z means it's referring to this run's initial snapshot)
    gas_ids_z = part_z['gas']['id']
    
    
    gas_gen_z = part_z['gas']['id.generation']
    gas_child_z = part_z['gas']['id.child']
    gas_den_z = part_z['gas']['density']
    selection_z = (gas_gen_z == 0) & (gas_child_z == 0)
    
    
    #this quantity is all of the gas IDs at future snapshot that I'm interested in
    gas_ids_selected_z = gas_ids_z[selection_z]
    gas_den_selected_z = gas_den_z[selection_z]*((MsunToGm/KpcToCm**3)/mp)
    gas_ids_selected_z_sorted = np.sort(gas_ids_selected_z)
    loc = np.searchsorted(ids[:,0],gas_ids_selected_z)
    
    ids[loc,i+1] = gas_ids_selected_z
    den[loc,i+1] = gas_den_selected_z
    
    
    ### now den and ids are properly sorted ###
    print(ids[45,i+1])
    print(den[45,i+1])
    print(min(den[:,i+1]))
    print(max(den[:,i+1]))
    becomes_dense = np.where(den[:,i+1] == 0)[0] #a list of all gas with null den (became star) at snapshot i+1 (i+1 because den[0] already put in and i starts at 0)
    #becomes_dense = becomes_dense.astype('int')
    
    print(len(destined))
    print(becomes_dense)
    print(len(becomes_dense))
    
    becomes_diffuse = np.where(den[:,i+1] < den_min)[0] #a list of all gas currently diffuse in current snapshot
    #becomes_diffuse.astype('int')
    print(becomes_diffuse)
    print(len(becomes_diffuse))

    #josh's non loop version:
    # is_becoming_dense = (destined == 1) & (den[:, i+1] == 0)
    #did anything become dense?
    # yes_something_got_dense = np.sum(is_becoming_dense) > 0
    # if yes_something_got_dense:
    # you may eed to deal with extend?
    #     is_dense.append(ids[yes_something_got_dense,i+1])
     
     
    for j in range(len(destined)):
        if destined[j] == 1:
            if (R_0[j] < 20) & (z[j] > -5) & (z[j] < 5):
                if den[j,i+1] == 0:
                    is_dense.append(ids[j,0])
                    inst_is_dense.append(den[j,0])
                
                    if ((z[j] > 0) & (v_z[j] > 0)) or ((z[j] < 0) & (v_z[j] < 0)):
                        outflow_v_z_inst_is_dense.append(den[j,0])
                        destined[j] = 0
                    elif ((z[j] < 0) & (v_z[j] > 0)) or ((z[j] > 0) & (v_z[j] < 0)):
                        inflow_v_z_inst_is_dense.append(den[j,0])
                        destined[j] = 0
                
            
                elif den[j,i+1] < den_min:
                    is_diffuse.append(ids[j,0])
                    inst_is_diffuse.append(den[j,0])
                
                    if ((z[j] > 0) & (v_z[j] > 0)) or ((z[j] < 0) & (v_z[j] < 0)):
                        outflow_v_z_inst_is_diffuse.append(den[j,0])
                        destined[j] = 0
                    elif ((z[j] < 0) & (v_z[j] > 0)) or ((z[j] > 0) & (v_z[j] < 0)):
                        inflow_v_z_inst_is_diffuse.append(den[j,0])
                        destined[j] = 0

    
    
    np.savetxt(outpath + 'ids/' + 'ids_velocity_' + str(start + i +1) + '.txt', ids[:,i+1])
    #is_dense = np.unique(is_dense)
    #is_diffuse = np.unique(is_diffuse)
    
    #print(is_dense)
    print(ids[np.where(den[:,i+1] == 0)[0],i+1])
    
    print(np.where(den[:,i+1] == 0)[0])
    print(len(destined))
    print(len(den[:,i+1]))

    print(destined)
    print(len(is_diffuse))
    print(len(is_dense))
    
    
    
    
    
    
    
    print(len(np.where(den[:,i+1] < den_min)[0]))
    
    #destined[np.where(becomes_dense != 0)[0]] = 0 #marking off location of ids that have reached a destiny
    #destined[np.where(becomes_diffuse != 0)[0]] = 0
    t_t2 = t.time()
    print(t_t2 - t_t1)
    print(len(np.where(ids[:,0] != ids[:,i+1])[0]))

print(ids[0:0])
print(ids[1,0])
print(den[0,0])
print(den[1,0])

print(len(ids[:,0]))
print(max(ids[:,0]))
print(den[:,0])

np.savetxt(outpath + 'ids/' + 'dense_ids_velocity_' + str(start) + '_' + str(end) + '.txt', is_dense)
np.savetxt(outpath + 'ids/' + 'diffuse_ids_velocity_' + str(start) + '_' + str(end) + '.txt', is_diffuse)

    

#for i in range(len(is_dense)):
#    inst_is_dense.append(den[np.where(ids[:,0] == is_dense[i])[0],0])

#print(len(inst_is_dense))


#for i in range(len(is_diffuse)):
#    inst_is_diffuse = den[np.where(ids[:,0] == is_diffuse[i])[0], 0] 
#print(len(inst_is_diffuse))             
#where does this become dense or diffuse
#save true or false of if became dense or diffuse
#before where, see if when becomes dense

# In[ ]:


outfilename = sstart + '_'+ send + '.txt'


np.savetxt(outpath + 'destined_velocity' + sstart + '_' + send + '.txt', destined)

np.savetxt(outpath + 'dense_outflow_v_z' + outfilename, outflow_v_z_inst_is_dense)
np.savetxt(outpath + 'diffuse_outflow_v_z' + outfilename, outflow_v_z_inst_is_diffuse)

np.savetxt(outpath + 'dense_inflow_v_z' + outfilename, inflow_v_z_inst_is_dense)
np.savetxt(outpath + 'diffuse_inflow_v_z' + outfilename, inflow_v_z_inst_is_diffuse)

np.savetxt(outpath + 'ids/' + 'dense_ids_velocity_' + str(start) + '_' + str(end) + '.txt', is_dense)
np.savetxt(outpath + 'ids/' + 'diffuse_ids_velocity_' + str(start) + '_' + str(end) + '.txt', is_diffuse)


#print(len(np.unique(inst_is_dense)))
#print(len(np.unique(inst_is_diffuse)))
