import argparse

from utils.dimacs import read_all_leaf_features
from utils.index import print_index_dictionary
from utils.utils import pickle_save

ROOT_PATH = '../../data/<kb_name>'

INVALID_CONF_FILE = '%s/conflict/invalid_confs/txt/invalid_conf_1_1.txt' % ROOT_PATH
INDEX_FILE = '%s/kb/<kb_name>_leaf.index' % ROOT_PATH

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='Create index file',
                                     description='Create index file.')
    parser.add_argument('--kb_name', type=str,
                        help='Knowledge base name - busybox')
    args = parser.parse_args()

    kb_name = args.kb_name
    ROOT_PATH = ROOT_PATH.replace('<kb_name>', kb_name)

    invalid_conf_file = INVALID_CONF_FILE.replace('<kb_name>', kb_name)
    index_file = INDEX_FILE.replace('<kb_name>', kb_name)

    # read all leaf features from an invalid configuration file
    # feature_map = read_all_leaf_features(INVALID_CONF_FILE)
    feature_map = read_all_leaf_features(invalid_conf_file)
    # read all variables from dimacs file into a feature_map dictionary
    # feature_map = read_all_variables(DIMACS_FILE)

    # print the feature_map dictionary
    print_index_dictionary(feature_map)

    # Save the feature_map dictionary into a file
    # index_file = DIMACS_FILE.replace('.dimacs', '_leaf.index')
    pickle_save(feature_map, index_file)