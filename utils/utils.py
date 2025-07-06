"""
MIGRATED to conflict-diagnosis-learning-benchmark repository
"""

import csv
import pickle
from enum import Enum
from typing import List, Tuple

CONFLICT_FILE_DELIMITER = ' --- '
ASSIGNMENT_CONFLICT_FILE_DELIMITER = '='
ASSIGNMENT_CONF_FILE_DELIMITER = ' '

class OutputType(Enum):
    ONE_HOT = 1
    NORMAL = 0

class FileType(Enum):
    CONFIGURATION = 0
    CONFLICT = 1

def read_paths_file(path: str) -> List[Tuple[str, str]]:
    invalid_conf_paths = []
    conflict_paths = []
    with open(path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            invalid_conf_paths.append(row[0])
            conflict_paths.append(row[1])
    return list(zip(invalid_conf_paths, conflict_paths))


def write_data_to_csv(data: List[List[object]], path: str) -> None:
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def pickle_save(data: object, path: str) -> None:
    with open(path, 'wb') as f:
        pickle.dump(data, f)


def read_text_file(path: str, startswith: str = None) -> List[str]:
    """
    Read a text file and return all lines
    :param startswith: the line should start with this string
    :param path: path to the file
    :return: all lines in the file
    """
    with open(path, 'r') as file:
        # read all lines
        lines = file.readlines()
        if startswith is None:
            return lines
        return [line for line in lines if line.startswith(startswith)]


# TODO check with other apps
def read_and_split(path: str, file_type: FileType) -> List[List[str]]:
    """
    Read and split a file into a list of lists of strings
    # To read allConflictSets.da, use delimiter = ' --- '.
    # To read a configuration file, use delimiter = ' '.
    :param file_type: configuration file / conflict file
    :param path: path to the file
    :return: a list of lists of strings
    """
    lines = read_text_file(path)

    if file_type == FileType.CONFLICT:
        return split(lines)
    return split_assignments(lines, ASSIGNMENT_CONF_FILE_DELIMITER)


def split_assignments(lines: List[str], delimiter: str) -> List[List[str]]:
    all_lines = []
    for line in lines:
        elements = line.strip().rsplit(delimiter, 1)

        # elements = line.strip().split(delimiter)
        all_lines.append(elements)
    return all_lines


def split(conflicts: List[str]) -> List[List[str]]:
    """
    Split a conflict string into a list of strings
    :param conflicts: a list of conflicts
    :return: a list of strings
    """
    lines = [conflict.strip().split(CONFLICT_FILE_DELIMITER) for conflict in conflicts]
    if len(lines) == 1:
        lines = lines[0]

    return split_assignments(lines, ASSIGNMENT_CONFLICT_FILE_DELIMITER)


def print_first_n_vectors(data: List[List[int]], n: int) -> None:
    if n > len(data):
        n = len(data)
    for i in range(n):
        print(data[i])


def print_first_n_items(data: List[object], n: int) -> None:
    if n > len(data):
        n = len(data)
    for i in range(n):
        print(data[i])


def assert_correct_convert(file: str, assignments: List[List[str]], vector: List[int], file_type: FileType) -> None:
    """
    Check if the number of 1, -1, and 0 in the configuration file / conflict file
    is the same as the number of 1, -1, and 0 in the conf_vector / conflict_vector
    :param file_type: configuration file / conflict file
    :param file: the configuration file / conflict file
    :param assignments: a list of assignments
    :param vector: conf_vector / conflict_vector
    """
    one_counter = 0
    minus_one_counter = 0

    for elements in assignments:
        # TODO: support for one-hot
        # if output_type == OutputType.ONE_HOT:  # one-hot
        #     # merge two elements into one
        #     feature = "=".join(elements)
        #     # if feature not in feature_map:
        #     #     print(f'{feature} not found in feature_map, {invalid_conf_path}')
        #     # print(f'{feature}: {feature_map.get(feature, "NO")}')
        # else:  # normal
        # feature = elements[0]
        value = elements[1]

        # for testing
        if value == 'true':
            one_counter += 1
        elif value == 'false':
            minus_one_counter += 1

    one_in_conf_vector = vector[1:].count(1)  # count how many 1 in conf_vector, except the first element
    minus_one_in_conf_vector = vector[1:].count(-1)  # count how many -1 in conf_vector, except the first element
    zero_in_conf_vector = vector[1:].count(0)  # count how many 0 in conf_vector, except the first element
    # check if the number of 1, -1, and 0 in conf_vector
    # is the same as the number of 1, -1, and 0 in the configuration file
    assert one_counter == one_in_conf_vector, (f'file: {file}, '
                                               f'one_counter: {one_counter}, '
                                               f'one_in_conf_vector: {one_in_conf_vector}')
    assert minus_one_counter == minus_one_in_conf_vector, (f'conf_file: {file}, '
                                                           f'minus_one_counter: {minus_one_counter}, '
                                                           f'minus_one_in_conf_vector: {minus_one_in_conf_vector}')
    if file_type == FileType.CONFIGURATION:
        assert zero_in_conf_vector == 0, (f'file: {file}, '
                                          f'zero_in_conf_vector: {zero_in_conf_vector}')
    elif file_type == FileType.CONFLICT:
        assert zero_in_conf_vector == (len(vector) - 1 - one_counter - minus_one_counter), \
            f'file: {file}, zero_in_conf_vector: {zero_in_conf_vector}'