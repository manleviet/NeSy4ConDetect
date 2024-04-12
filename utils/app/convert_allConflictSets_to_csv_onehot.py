from utils.utils import write_data_to_csv, read_and_split
from utils.index import read_index

ROOT_PATH = '../../data/busybox'

MODEL_INDEX_FILE = '%s/kb/busybox_onehot.index' % ROOT_PATH
ALL_CONFLICT_SETS_FILE = '%s/conflict/allConflictSets.da' % ROOT_PATH

# load the feature_map dictionary from the index file
feature_map = read_index(MODEL_INDEX_FILE)

# print the feature_map
# print_dictionary(feature_map)

all_cs_vectors = []
# read all conflict sets in allConflictSets.da file
all_cs = read_and_split(ALL_CONFLICT_SETS_FILE, ' --- ')
# loop through all cs
for cs in all_cs:
    print(cs)

    # create a vector of all 0 values
    cs_vector = [0] * len(feature_map)
    # loop through all constraints in cs
    for cstr in cs:
        # print the feature index if it exists, otherwise print 'NO'
        print(f'{cstr}: {feature_map.get(cstr, "NO")}')
        index: int = feature_map.get(cstr, None)
        # set 1 to the feature index
        if index is not None:
            cs_vector[index] = 1

    # print the conflict set
    print(cs_vector)

    # append the conflict set to all_cs
    all_cs_vectors.append(cs_vector)

# save all_cs to a csv file
all_conflict_sets_csv_onehot_file = ALL_CONFLICT_SETS_FILE.replace('.da', '_onehot.csv')
write_data_to_csv(all_cs_vectors, all_conflict_sets_csv_onehot_file)

