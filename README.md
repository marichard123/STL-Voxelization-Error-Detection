# STL-Voxelization-Error-Detection
Files written during URAP Fall 2022 undergraduate research to detect STL files that fail to voxelize properly. 

This repository is meant to be used alongside my [rotation and voxelization pipeline](https://github.com/marichard123/Voxelization-and-Rotation-Pipeline), but can be run alone. The files make heavy use of [binvox.exe](https://www.patrickmin.com/binvox), written by Patrick Min.


# What it does:
This package will, given a directory containing STL files, will output a CSV file listing all STL files that failed to properly voxelize through binvox. The CSV file will list one of three ways that each file failed—through the STL file originally being empty, through a thin STL model voxelizing into an empty voxelization, or through the voxelization becoming discontinous. This package will give insight into the STL files used to in the rotation and voxelization pipeline. This package has been kept separate from the rotation and voxelization pipeline for runtime reasons. 


# How to use it:
To download and make use of the pipeline, the entire STL-Voxelization-Error-Detection repository should be downloaded as a zip file and unzipped. Once installed, there are only two steps to using the pipeline:

1). **The STL files to be voxelized and rotated should be moved inside a folder called 'stl_repository', which is to be located inside the Voxelization-and-Rotation-Pipeline directory.** A zipped 'stl_repository' folder is included, with several sample STL files inside of it. Once unzipped, the pipeline is ready to run, and STL files may be added to the 'stl_repository' folder as desired. Alternatively, a pathway to an alternative pipeline of a different name may be specified—the next step will describe this process.

2). **The 'detecting_failed_files_user_interface.m' MatLab file should be run. If the user wishes to run the file under default settings (to be explained), then no further action or manipulation is required.** The alterable parameters are located in lines 2-5 in 'detecting_failed_files_user_interface.m'. By default, STL files are read from the 'stl_repository' directory, and the filename of the output CSV file is set to 'Failed_Files.csv'. By default, 'default_voxelization' is set to false, meaning that STL files will be voxelized to 64^3 dimension when testing. If 'default_voxelization' is set to true, then STL files will be voxelized to default (256^3) dimension when testing. By default, 'exact_continuity_test' = true, meaning that the continuity of the 3D voxel image will be exactly calculated. If 'exact_continuity_test' is set to false, then the image will be approximated as three 2D images projected onto all three axes, significantly reducing runtime but allowing for the possibility of false positives. 
  Setting 'default_voxelization' to true will considerably increase runtime. It is strongly recommended that the exact continuity test not be used with default voxelization, as runtime will likely become infeasibly slow on most machines.
