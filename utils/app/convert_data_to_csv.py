"""
Read data from both conflict and diagnosis folders
Convert the data to vectors
"""
import argparse

from utils.utils import read_paths_file, write_data_to_csv, print_first_n_vectors, OutputType
from utils.vector import convert_conf_to_vector, convert_conflict_to_vector
from utils.index import read_index, print_index_dictionary

ROOT_PATH = '../../data/<kb_name>'

MODEL_INDEX_FILE = '%s/kb/<kb_name>_leaf.index' % ROOT_PATH
DIAGNOSIS_PATHS_FILE = '%s/diagnosis/invalid_confs/invalid_conf_paths.txt' % ROOT_PATH
CONFLICT_PATHS_FILE = '%s/conflict/invalid_confs/invalid_conf_paths.txt' % ROOT_PATH

CONFLICTS_OUTPUT_PATH = '%s/conflicts.csv' % ROOT_PATH
INVALID_CONFS_OUTPUT_PATH = '%s/invalid_confs.csv' % ROOT_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Create data to csv',
                                     description='Create data to csv.')
    parser.add_argument('--kb_name', type=str,
                        help='Knowledge base name - busybox')
    args = parser.parse_args()

    kb_name = args.kb_name
    ROOT_PATH = ROOT_PATH.replace('<kb_name>', kb_name)
    MODEL_INDEX_FILE = MODEL_INDEX_FILE.replace('<kb_name>', kb_name)
    DIAGNOSIS_PATHS_FILE = DIAGNOSIS_PATHS_FILE.replace('<kb_name>', kb_name)
    CONFLICT_PATHS_FILE = CONFLICT_PATHS_FILE.replace('<kb_name>', kb_name)
    CONFLICTS_OUTPUT_PATH = CONFLICTS_OUTPUT_PATH.replace('<kb_name>', kb_name)
    INVALID_CONFS_OUTPUT_PATH = INVALID_CONFS_OUTPUT_PATH.replace('<kb_name>', kb_name)

    # load the feature_map dictionary from index file
    feature_map = read_index(MODEL_INDEX_FILE)

    # # print the feature_map
    # print_index_dictionary(feature_map)

    invalid_conf_vectors = []
    conflict_vectors = []
    conf_id = 0
    total_conflicts = 0

    # CONFLICT
    # read the paths file
    paths = read_paths_file(CONFLICT_PATHS_FILE)

    for invalid_conf_file, conflict_file in paths:
        invalid_conf_vector = convert_conf_to_vector(invalid_conf_file, feature_map, conf_id, OutputType.NORMAL)
        invalid_conf_vectors.append(invalid_conf_vector)

        conflict_vector = convert_conflict_to_vector(0, conflict_file, feature_map, conf_id, OutputType.NORMAL)
        conflict_vectors.append(conflict_vector)

        conf_id += 1
        total_conflicts += 1

    # DIAGNOSIS
    # read the paths file
    paths = read_paths_file(DIAGNOSIS_PATHS_FILE)

    for invalid_conf_file, conflict_file in paths:
        invalid_conf_vector = convert_conf_to_vector(invalid_conf_file, feature_map, conf_id, OutputType.NORMAL)

        # read the conflict file
        with open(conflict_file, 'r') as file:
            for j, line in enumerate(file):
                # If the line number is greater than or equal to 5 (6th line), print the line
                if j >= 5:
                    # print(line.strip())
                    conflict_vector = convert_conflict_to_vector(1, line, feature_map, conf_id, OutputType.NORMAL)

                    invalid_conf_vectors.append(invalid_conf_vector)
                    conflict_vectors.append(conflict_vector)

                    total_conflicts += 1

        conf_id += 1

    print(f'Total configurations: {len(invalid_conf_vectors)}')
    print(f'Total line of conflicts: {len(conflict_vectors)}')

    # print the first 5 invalid configurations
    print_first_n_vectors(invalid_conf_vectors, 5)
    # print the first 5 conflict vectors
    print_first_n_vectors(conflict_vectors, 5)

    # save
    write_data_to_csv(invalid_conf_vectors, INVALID_CONFS_OUTPUT_PATH)
    write_data_to_csv(conflict_vectors, CONFLICTS_OUTPUT_PATH)
