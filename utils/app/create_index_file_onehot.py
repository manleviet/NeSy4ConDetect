from utils.dimacs import read_all_variables_onehot
from utils.utils import pickle_save, read_text_file
from utils.index import print_index_dictionary

ROOT_PATH = '../../data/busybox'

DIMACS_FILE = '%s/kb/busybox.dimacs' % ROOT_PATH

# read all variables from dimacs file into a feature_map dictionary
feature_map = read_all_variables_onehot(DIMACS_FILE)

# print the feature_map dictionary
print_index_dictionary(feature_map)

# Save the feature_map dictionary into a file
index_file = DIMACS_FILE.replace('.dimacs', '_onehot.index')
pickle_save(feature_map, index_file)
