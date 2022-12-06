# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 04:00:19 2022

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
def two_dimension_approximation(real_indices):
    starting_index = int(math.floor(len(real_indices))/2)
    infected_indices = np.array([real_indices[starting_index]])
    previous_length = 0
    #for ii in range (50):
    while (infected_indices.shape != previous_length):
        preloop_infected_indices = copy.deepcopy(infected_indices)
        previous_length = preloop_infected_indices.shape
        #print(preloop_infected_indices.shape)
        for x_shift in range(-1,2):
            for y_shift in range(-1,2):
                if not (x_shift ==0 and y_shift==0):
                    shifted_x_indices = preloop_infected_indices[:,0] + x_shift
                    shifted_y_indices = preloop_infected_indices[:,1] + y_shift
                        
                        
                    shifted_indices = np.stack((shifted_x_indices, shifted_y_indices), axis = 1)
                        
                        
                    #intersecting_values = np.array([x for x in set(tuple(x) for x in real_indices) & set(tuple(x) for x in shifted_indices)])
                    #shifted_indices = copy.deepcopy(intersecting_values)
                    #print(shifted_indices.size)
                    if shifted_indices.size > 0:
                        infected_indices = np.vstack([infected_indices, shifted_indices])
                        
        #print('starting for loop')
        
        intersecting_values = np.array([x for x in set(tuple(x) for x in real_indices) & set(tuple(x) for x in infected_indices)])
        infected_indices = copy.deepcopy(intersecting_values)
        
        unique_values = np.unique(infected_indices, axis = 0)
        infected_indices = copy.deepcopy(unique_values)
        #print(infected_indices.shape)
    return infected_indices
#real_indices = np.stack((real_x_indices, real_y_indices, real_z_indices), axis = 1)

#XY plane
real_indices = np.stack((real_x_indices, real_y_indices), axis = 1)
unique_values = np.unique(real_indices, axis = 0)
real_indices = copy.deepcopy(unique_values)
print(real_indices.shape)
infected_indices = two_dimension_approximation(real_indices)
print(infected_indices.shape)
if infected_indices.shape != real_indices.shape:
    raise ValueError('Voxelized image is discontinous, considering face and edge contact')
del real_indices
del unique_values
del infected_indices
print(" ")
#XZ plane
real_indices = np.stack((real_x_indices, real_z_indices), axis = 1)
unique_values = np.unique(real_indices, axis = 0)
real_indices = copy.deepcopy(unique_values)
print(real_indices.shape)
infected_indices = two_dimension_approximation(real_indices)
print(infected_indices.shape)
if infected_indices.shape != real_indices.shape:
    raise ValueError('Voxelized image is discontinous, considering face and edge contact')
del real_indices
del unique_values
del infected_indices
print(" ")
#YZ plane
real_indices = np.stack((real_y_indices, real_z_indices), axis = 1)
unique_values = np.unique(real_indices, axis = 0)
real_indices = copy.deepcopy(unique_values)
print(real_indices.shape)
infected_indices = two_dimension_approximation(real_indices)
print(infected_indices.shape)
if infected_indices.shape != real_indices.shape:
    raise ValueError('Voxelized image is discontinous, considering face and edge contact')