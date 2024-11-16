"""
prepare list of paths for all invalid configuration files
each line is a pair of invalid configuration file path and the corresponding conflict file path
"""
import argparse
import os

from utils.utils import print_first_n_items, write_data_to_csv

ROOT_PATH = '../../data/<kb_name>/conflict/invalid_confs'

OUTPUT_FILE = '%s/invalid_conf_paths.txt' % ROOT_PATH

# exclude_numbers = [30, 39, 47, 49, 52, 53, 67, 70, 75, 76, 79, 84, 86, 91, 93, 101, 102, 108, 109, 113, 118, 119, 129,
#                    132, 133, 139, 141, 143, 149, 153]
INPUT_PATH = '%s/txt/' % ROOT_PATH
invalid_conf = 'invalid_conf_'
original_cs = 'original_cs_'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Create invalid conf paths file for conflict',
                                     description='Create invalid conf paths file for conflict.')
    parser.add_argument('--kb_name', type=str,
                        help='Knowledge base name - busybox')
    args = parser.parse_args()

    kb_name = args.kb_name
    ROOT_PATH = ROOT_PATH.replace('<kb_name>', kb_name)
    INPUT_PATH = INPUT_PATH.replace('<kb_name>', kb_name)
    OUTPUT_FILE = OUTPUT_FILE.replace('<kb_name>', kb_name)

    invalid_conf_paths = []
    original_cs_paths = []

    for i in range(1, 143):
        # if i in exclude_numbers:
        #     continue
        for j in range(1, 6):
            invalid_conf_path = INPUT_PATH + invalid_conf + str(i) + '_' + str(j) + '.txt'
            if not os.path.exists(invalid_conf_path):
                print('File does not exist: ' + invalid_conf_path)
                continue

            invalid_conf_paths.append(invalid_conf_path)
            original_cs_paths.append(INPUT_PATH + original_cs + str(i) + '_' + str(j) + '.txt')

    # print the first 5 invalid_conf_paths and original_cs_paths
    print_first_n_items(invalid_conf_paths, 5)
    print_first_n_items(original_cs_paths, 5)

    # save the invalid_conf_paths and original_cs_paths to a text file
    paths = list(zip(invalid_conf_paths, original_cs_paths))
    write_data_to_csv(paths, OUTPUT_FILE)
