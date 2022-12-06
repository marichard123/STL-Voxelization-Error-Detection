# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 23:38:26 2022

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
if real_indices.size == 0:
    raise ValueError('Voxel image is empty')