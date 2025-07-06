"""
MIGRATED to conflict-diagnosis-learning-benchmark repository
"""

from typing import Dict, List

from utils.utils import read_and_split, assert_correct_convert, OutputType, FileType, split


# TODO: fix ONE_HOT
def convert_conf_to_vector(conf_file: str, feature_map: Dict[str, int], conf_id: int, output_type: OutputType) \
        -> List[int]:
    """
    Convert a configuration file to a vector
    :param output_type: OutputType.ONE_HOT - one-hot, OutputType.NORMAL - normal
    :param conf_file: path to the configuration file
    :param feature_map: if output_type==1: a one-hot feature map, otherwise a normal feature map
    :param conf_id: configuration id
    :return: a vector
    """
    conf_vector = [0] * (len(feature_map) + 1)
    conf_vector[0] = conf_id

    # read the configuration file
    assignments = read_and_split(conf_file, FileType.CONFIGURATION)
    convert_assignments_to_vector(assignments, conf_file, conf_vector, feature_map, output_type)

    # check if the number of 1, -1, and 0 in the configuration file
    # is the same as the number of 1, -1, and 0 in the conf_vector
    assert_correct_convert(conf_file, assignments, conf_vector, FileType.CONFIGURATION)

    return conf_vector

# TODO: fix ONE_HOT
def convert_assignments_to_vector(assignments: List[List[str]], file: str, vector: List[int],
                                  feature_map: Dict[str, int], output_type: OutputType) -> None:
    """
    Convert a list of assignments to a vector
    :param assignments: a list of assignments
    :param file: the configuration file / conflict file
    :param vector: conf_vector / conflict_vector
    :param feature_map: a feature map
    :param output_type: OutputType.ONE_HOT - one-hot, OutputType.NORMAL - normal
    """
    for elements in assignments:
        if output_type == OutputType.ONE_HOT:  # one-hot
            # merge two elements into one
            feature = "=".join(elements)
        else:  # normal
            feature = elements[0]
            value = elements[1]

        # get the index of the feature
        index = feature_map.get(feature, None)
        assert index is not None, f'{feature} not found in feature_map, {file}'

        # set 1 or -1 to the feature index
        if output_type == OutputType.ONE_HOT:
            vector[int(index)] = 1
        else:
            # 1 if true, -1 if false, 0 if not present
            vector[int(index)] = 1 if (elements[1] == 'true') else -1


# TODO: fix ONE_HOT
def convert_conflict_to_vector(source_type: int, conflict_file: str, feature_map: Dict[str, int],
                               conf_id: int, output_type: OutputType) \
        -> List[int]:
    """
    Convert a conflict file to a one-hot vector
    :param output_type: OutputType.ONE_HOT - one-hot, OutputType.NORMAL - normal
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
        assignments = read_and_split(conflict_file, FileType.CONFLICT)
    else:
        assignments = split([conflict_file])
    convert_assignments_to_vector(assignments, conflict_file, conflict_vector, feature_map, output_type)

    # check if the number of 1, -1, and 0 in conflict_vector
    # is the same as the number of 1, -1, and 0 in the conflict file
    assert_correct_convert(conflict_file, assignments, conflict_vector, FileType.CONFLICT)

    return conflict_vector
