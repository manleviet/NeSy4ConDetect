import pickle

# read all variables from dimacs file
# open the file
with open('../../data/busybox/busybox.dimacs', 'r') as file:
    # read all lines
    lines = file.readlines()

# create a dictionary to store the feature map
feature_map = {}
for line in lines:
    if line.startswith('c'):
        # split the line into elements
        elements = line.strip().split()
        if len(elements) >= 3:
            # key - third element, the name of the feature
            # value -second element, the index of the feature
            feature_map[elements[2]] = int(elements[1])

# print the feature_map dictionary
for key, value in feature_map.items():
    print(f'{key}: {value}')

# Save the feature_map dictionary into a file
with open('../../data/busybox/busybox.index', 'wb') as f:
    pickle.dump(feature_map, f)
