"""
prepare list of paths for all invalid configuration files
each line is a pair of invalid configuration file path and the corresponding conflict file path
"""
import os

from utils.utils import print_first_n_items, write_data_to_csv

ROOT_PATH = '../../data/busybox/diagnosis'
OUTPUT_FILE = '%s/invalid_confs/invalid_conf_paths.txt' % ROOT_PATH

sub_folders = ['1', '2', '4', '8', '16', '32']
INVALID_CONF_PATH = '%s/invalid_confs/txt/' % ROOT_PATH
COMBS_PATH = '%s/combs/comb_' % ROOT_PATH
invalid_conf = 'conf'
original_cs = 'original_diag'
invalid_conf_paths = []
original_diag_paths = []

# for each sub-folder
for sub_folder in sub_folders:
    sub_folder_path = INVALID_CONF_PATH + sub_folder + '/'
    comb_path_sub_folder = COMBS_PATH + sub_folder + '/'
    # loop through all files whose name starts with 'conf'
    for file_name in os.listdir(sub_folder_path):
        if file_name.startswith('conf'):
            invalid_conf_paths.append(sub_folder_path + file_name)
            # take the part of the filename after '_'
            parts = file_name.split('_')
            new_filename = 'comb' + parts[1]
            original_diag_paths.append(comb_path_sub_folder + new_filename)

            if not os.path.exists(comb_path_sub_folder + new_filename):
                print('File does not exist: ' + comb_path_sub_folder + new_filename)

# print the first 5 invalid_conf_paths and original_cs_paths
print_first_n_items(invalid_conf_paths, 5)
print_first_n_items(original_diag_paths, 5)

# save the invalid_conf_paths and original_cs_paths to a text file
paths = list(zip(invalid_conf_paths, original_diag_paths))
write_data_to_csv(paths, OUTPUT_FILE)
