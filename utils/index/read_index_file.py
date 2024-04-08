import pickle

# load the feature_map dictionary from a file
with open('../../data/busybox/busybox.index', 'rb') as f:
    feature_map = pickle.load(f)

# print the feature_map
for key, value in feature_map.items():
    print(f'{key}: {value}')
