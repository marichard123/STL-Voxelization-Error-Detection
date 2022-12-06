# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 00:23:43 2022

@author: Richard
"""

import sys
import os
#From command line, read in the filename and whether to readjust an incorrectly oriented image
filename = sys.argv[1]
import binvox_rw_fastwrite2 as binvox_rw
import numpy as np
import math
import copy
with open(filename, 'rb') as f:
    model = binvox_rw.read_as_3d_array(f)
print("Voxelized model dimensions: " + str(model.dims))
print(filename)
a = np.ones([1], dtype=bool)
true_placeholder = copy.deepcopy(a[0])
true_indices = np.where(model.data==true_placeholder)
real_x_indices = true_indices[0]
real_y_indices = true_indices[1]
real_z_indices = true_indices[2]

real_indices = np.stack((real_x_indices, real_y_indices, real_z_indices), axis = 1)

#shifted_x_indices = real_indices[:,0] + 1
#shifted_y_indices = real_indices[:,1] + 0
#shifted_z_indices = real_indices[:,2] + 0
#                    
#shifted_indices = np.stack((shifted_x_indices, shifted_y_indices, shifted_z_indices), axis = 1)


#combination = np.vstack([real_indices, shifted_indices])
#print(combination)
#unique_values, counts = np.unique(combination, return_counts = True, axis = 0)

#for i in counts:
#    print(i)
combination = copy.deepcopy(real_indices)
for x_shift in range(-1,2):
        for y_shift in range(-1,2):
            for z_shift in range(-1,2):
                if not (x_shift ==0 and y_shift==0 and z_shift ==0):
                    shifted_x_indices = real_indices[:,0] + x_shift
                    shifted_y_indices = real_indices[:,1] + y_shift
                    shifted_z_indices = real_indices[:,2] + z_shift
                    shifted_indices = np.stack((shifted_x_indices, shifted_y_indices, shifted_z_indices), axis = 1)
                    combination = np.vstack([combination, shifted_indices])
                    
unique_values, counts = np.unique(combination, return_counts = True, axis = 0)
#print(np.where(counts == 27)[0])
interior_indices = np.where(counts == 27)[0]
#print(type(interior_indices))
interior_coordinates = unique_values[interior_indices]

combination_2 = np.vstack([real_indices, interior_coordinates])
unique_values_2, counts_2 = np.unique(combination_2, return_counts = True, axis = 0)
edge_indices = np.where(counts_2 == 1)[0]
edge_coordinates = unique_values_2[edge_indices]
print(edge_coordinates.shape)
print(real_indices.shape)