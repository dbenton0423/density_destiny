import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import gizmo_analysis as gizmo
import utilities as ut

MsunToGm = 1.99e33
KpcToCm  = 3.086e21
mp       = 1.67e-24

simdir='/scratch/04712/tg840119/m12i_m7e3_HD_fire3_fireBH_Sep052021_hr_crdiffc690_sdp1e10_gacc31_fa0.5'
snapnumber = 258
part = gizmo.gizmo_io.Read.read_snapshots(['gas'], 'index', snapnumber, simulation_directory=simdir, assign_hosts_rotation=True, assign_hosts=True)

id_gas     = part['gas']['id']

load_path         = 'feh/ids/'
diffuse_destinies = np.loadtxt(load_path + 'diffuse_ids_feh_475_501.txt')
print(len(diffuse_destinies))

import time as t
t1 = t.time()

diffuse_id_location = []


for i in range(1800000, 3018005):
    diffuse_id_location.append(np.where(diffuse_destinies[i] == id_gas)[0])
np.savetxt(load_path + 'diffuse_id_locations_part3', diffuse_id_location)
t2 = t.time()
print(str(t2 - t1))

