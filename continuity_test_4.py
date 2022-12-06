# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 02:16:07 2022

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
def hollow_out(real_indices):
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
    
    interior_indices = np.where(counts == 27)[0]
    
    interior_coordinates = unique_values[interior_indices]
    combination_2 = np.vstack([real_indices, interior_coordinates])
    unique_values_2, counts_2 = np.unique(combination_2, return_counts = True, axis = 0)
    edge_indices = np.where(counts_2 == 1)[0]
    edge_coordinates = unique_values_2[edge_indices]
    return edge_coordinates
#real_indices = copy.deepcopy(edge_coordinates)
print('Starting hollowing process')
real_indices = hollow_out(real_indices)
print('Hollowing process completed')

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
            for z_shift in range(-1,2):
                if not (x_shift ==0 and y_shift==0 and z_shift ==0):
                    shifted_x_indices = preloop_infected_indices[:,0] + x_shift
                    shifted_y_indices = preloop_infected_indices[:,1] + y_shift
                    shifted_z_indices = preloop_infected_indices[:,2] + z_shift
                    
                    shifted_indices = np.stack((shifted_x_indices, shifted_y_indices, shifted_z_indices), axis = 1)
                    
                    
                    #intersecting_values = np.array([x for x in set(tuple(x) for x in real_indices) & set(tuple(x) for x in shifted_indices)])
                    #shifted_indices = copy.deepcopy(intersecting_values)
                    #print(shifted_indices.size)
                    if shifted_indices.size > 0:
                        infected_indices = np.vstack([infected_indices, shifted_indices])
                    
    #print('starting for loop')
    
    intersecting_values = np.array([x for x in set(tuple(x) for x in real_indices) & set(tuple(x) for x in infected_indices)])
    
    #unique_infected_indices = np.unique(infected_indices, axis = 0)
    #combination = np.vstack([real_indices, unique_infected_indices])
    #unique_values, counts = np.unique(combination, return_counts = True, axis = 0)
    #intersecting_indices = np.where(counts == 2)[0]
    #intersecting_values_2 = unique_values[intersecting_indices]
    #infected_indices = copy.deepcopy(intersecting_values_2)
    infected_indices = copy.deepcopy(intersecting_values)
    
    unique_values = np.unique(infected_indices, axis = 0)
    infected_indices = copy.deepcopy(unique_values)
    print(infected_indices.shape)
    

if infected_indices.shape != real_indices.shape:
    raise ValueError('Voxelized image is discontinous, considering face and edge contact')