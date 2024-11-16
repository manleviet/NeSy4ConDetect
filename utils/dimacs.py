from typing import Dict

from utils.utils import read_text_file


def read_all_leaf_features(path: str) -> Dict[str, int]:
    """
    Read all leaf features from an invalid configuration file
    :param path: path to the file
    :return: a dictionary with key as the leaf feature name and value as the leaf feature index
    """
    lines = read_text_file(path)

    feature_map = {}
    # loop through all lines
    index = 0
    for line in lines:
        # split the line into two elements
        elements = line.strip().rsplit(' ', 1)
        if len(elements) >= 2:
            # key - first element, the name of the leaf feature
            index += 1
            feature_map[elements[0]] = index

    return feature_map

def read_all_variables(path: str) -> Dict[str, int]:
    """
    Read all variables from a .dimacs file
    :param path: path to the file
    :return: a dictionary with key as the variable name and value as the variable index
    """
    lines = read_text_file(path, startswith='c')

    feature_map = {}
    # loop through all lines
    for line in lines:
        # split the line into elements
        elements = line.strip().split()
        if len(elements) >= 3:
            # key - third element, the name of the variable
            # value - second element, the index of the variable
            feature_map[elements[2]] = int(elements[1])

    return feature_map

# TODO fix for leaf features
def read_all_variables_onehot(path: str) -> Dict[str, int]:
    """
    Read all variables from a .dimacs file
    :param path: path to the file
    :return: a dictionary with key as an assignment and value as the assignment index
    """
    lines = read_text_file(path, startswith='c')

    feature_map = {}
    count = 1
    for line in lines:
        # split the line into elements
        elements = line.strip().split()
        if len(elements) >= 3:
            # key - third element, the name of the feature
            # create two variants of the key: key=true and key=false
            key1 = f'{elements[2]}=true'
            key2 = f'{elements[2]}=false'

            # key - third element, the name of the feature
            # value -second element, the index of the feature
            feature_map[key1] = count
            feature_map[key2] = count + 1
            count += 2

    return feature_map
