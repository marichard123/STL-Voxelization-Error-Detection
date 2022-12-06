function detecting_failed_files_approximation_function(stl_directory_name, default_voxelization, filename)
stl_files_directory = stl_directory_name;
output_filename = filename;

dinfo = dir(stl_files_directory);
stl_filenames = {dinfo.name};
stl_filenames = sort(stl_filenames);

OutputCellArray = {};
OutputCellArray{end+1,1} = 'Filename';
OutputCellArray{end,2} = 'Failed to Voxelize';
OutputCellArray{end,3} = 'Empty Voxelization';
OutputCellArray{end,4} = 'Discontinuous (Edge Criterion)';


for i = 3:length(stl_filenames)
    filename = stl_filenames{i};
    failed_to_voxelize = false;
    empty_voxelization = false;
    discontinuous_edge = false;
    
    disp(filename)
    full_pathway = [stl_files_directory, '\', filename];
    binvox_pathway = [full_pathway(1:end-4), '.binvox'];
    
    %Voxelization Test
    if default_voxelization
        command = ['binvox ',full_pathway];
    else
        command = ['binvox -d 64 ',full_pathway];
    end
    system(command)
    if ans == 1
        failed_to_voxelize = true;
    end
    
    %Emptiness Test
    if ~failed_to_voxelize
        command = ['python empty_voxelization_test.py ', binvox_pathway];
        system(command)
        if ans ==1
            empty_voxelization = true;
        end
    end
    
    %Edge continuity test
    if ~empty_voxelization && ~failed_to_voxelize
        command = ['python continuity_test_2D.py ', binvox_pathway];
        system(command)
        if ans ==1
            discontinuous_edge = true;
        end
    end
    
    
    
    %Getting rid of the binvox file after we're done with it
    if ~failed_to_voxelize
        command = ['del ' binvox_pathway];
        system(command)
    end
    %Adding a column if one of the criteria is met
    if failed_to_voxelize || empty_voxelization || discontinuous_edge
        OutputCellArray{end+1,1} = filename;
        OutputCellArray{end,2} = failed_to_voxelize;
        OutputCellArray{end,3} = empty_voxelization;
        OutputCellArray{end,4} = discontinuous_edge;
    end
    
    
end
disp(OutputCellArray);
output_filename = [output_filename, '.csv'];
writecell(OutputCellArray, output_filename);
end