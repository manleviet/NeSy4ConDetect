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
            # second element is the index of the feature
            # third element is the name of the feature
            feature_map[int(elements[1])] = elements[2]

# print the feature_map dictionary
for key, value in feature_map.items():
    print(f'{key}: {value}')

# Save the feature_map dictionary into a file
with open('../../data/busybox/busybox.index', 'wb') as f:
    pickle.dump(feature_map, f)
