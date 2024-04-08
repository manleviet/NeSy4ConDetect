import pickle
import csv

# load the feature_map dictionary from a file
with open('../data/busybox/busybox.index', 'rb') as f:
    feature_map = pickle.load(f)

# print the feature_map
# for key, value in feature_map.items():
#     print(f'{key}: {value}')

# read all conflict sets in allConflictSets.da file
# open the file
with open('../data/busybox/conflict/allConflictSets.da', 'r') as file:
    # read all lines
    lines = file.readlines()

all_cs = []
# loop through all lines
for line in lines:
    # split the line into elements
    elements = line.strip().split(' --- ')
    print(elements)
    # create a list of all null values
    cs = [None] * len(feature_map)
    # loop through all elements
    for element in elements:
        # split the element into variables
        sub_elements = element.split('=')
        # print the feature index if it exists, otherwise print 'NO'
        print(f'{sub_elements[0]}: {feature_map.get(sub_elements[0], "NO")}')
        index = feature_map.get(sub_elements[0], None)
        # set 1 to the feature index
        if index is not None:
            cs[index - 1] = 1

    # print the conflict set
    print(cs)

    # append the conflict set to all_cs
    all_cs.append(cs)

# save all_cs to a csv file
with open('../data/busybox/conflict/allConflictSets.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(all_cs)

