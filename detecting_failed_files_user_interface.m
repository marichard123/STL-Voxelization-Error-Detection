clear all; close all; clc;
stl_directory_name = 'stl_repository';
filename = 'Failed Files';
default_voxelization = false;
exact_continuity_test = true;


if exact_continuity_test
    detecting_failed_files_exact_function(stl_directory_name,default_voxelization, filename);
else
    detecting_failed_files_approximation_function(stl_directory_name,default_voxelization, filename);
end