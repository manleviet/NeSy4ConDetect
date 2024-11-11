from utils.dimacs import read_all_variables, read_all_leaf_features
from utils.utils import pickle_save, read_text_file
from utils.index import print_index_dictionary

ROOT_PATH = '../../data/busybox'

DIMACS_FILE = '%s/kb/busybox.dimacs' % ROOT_PATH
INVALID_CONF_FILE = '%s/conflict/invalid_confs/txt/invalid_conf_1_1.txt' % ROOT_PATH

# read all leaf features from an invalid configuration file
feature_map = read_all_leaf_features(INVALID_CONF_FILE)
# read all variables from dimacs file into a feature_map dictionary
# feature_map = read_all_variables(DIMACS_FILE)

# print the feature_map dictionary
print_index_dictionary(feature_map)

# Save the feature_map dictionary into a file
index_file = DIMACS_FILE.replace('.dimacs', '_leaf.index')
pickle_save(feature_map, index_file)
