from enum import Enum
from typing import Dict, List

from utils.utils import read_and_split

class OutputType(Enum):
    ONE_HOT = 1
    NORMAL = 0

def convert_conf_to_vector(conf_file: str, feature_map: Dict[str, int], conf_id: int, output_type: OutputType) \
        -> List[int]:
    """
    Convert a configuration file to a vector
    :param output_type: 1 - one-hot, 0 - normal
    :param conf_file: path to the configuration file
    :param feature_map: if output_type==1: a one-hot feature map, otherwise a normal feature map
    :param conf_id: configuration id
    :return: a vector
    """
    conf_vector = [0] * (len(feature_map) + 1)
    conf_vector[0] = conf_id
    conf_vector[1] = 1  # root=true

    # read the configuration file
    all_assignments = read_and_split(conf_file, ' ')
    for elements in all_assignments:
        if output_type == OutputType.ONE_HOT:  # one-hot
            # merge two elements into one
            feature = "=".join(elements)
            # if feature not in feature_map:
            #     print(f'{feature} not found in feature_map, {invalid_conf_path}')
            # print(f'{feature}: {feature_map.get(feature, "NO")}')
        else:  # normal
            feature = elements[0]

        # get the index of the feature
        index = feature_map.get(feature, None)
        # set 1 to the feature index
        if index is not None:
            if output_type == OutputType.ONE_HOT:
                conf_vector[int(index)] = 1
            else:
                # 1 if true, -1 if false, 0 if not present
                conf_vector[int(index)] = 1 if (elements[1] == 'true') else -1

    return conf_vector


def convert_conflict_to_vector(source_type: int, conflict_file: str, feature_map: Dict[str, int],
                               conf_id: int, output_type: OutputType) \
        -> List[int]:
    """
    Convert a conflict file to a one-hot vector
    :param output_type: 1 - one-hot, 0 - normal
    :param source_type: 0 if conflict_file is a conflict file, 1 if conflict_file is a string of constraints
    :param conflict_file: path to the conflict file
    :param feature_map: if output_type==1: a one-hot feature map, otherwise a normal feature map
    :param conf_id: configuration id
    :return: a one-hot vector
    """
    conflict_vector = [0] * (len(feature_map) + 1)
    conflict_vector[0] = conf_id

    # read the conflict file
    if source_type == 0:
        elements = read_and_split(conflict_file, ' --- ')[0]
    else:
        elements = conflict_file.strip().split(' --- ')
    # print(elements)
    # loop through all elements
    for element in elements:
        value = 'false'
        if output_type == OutputType.NORMAL:
            parts = element.split('=')
            element = parts[0]
            value = parts[1]
        # # print the feature index if it exists, otherwise print 'NO'
        # print(f'{element}: {feature_map.get(element, "NO")}')

        index = feature_map.get(element, None)
        # set 1 to the feature index
        if index is not None:
            if output_type == OutputType.ONE_HOT:
                conflict_vector[int(index)] = 1
            else:
                # 1 if true, -1 if false, 0 if not present
                conflict_vector[int(index)] = 1 if (value == 'true') else -1

    return conflict_vector
