import csv
import pickle
from typing import List, Tuple


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


def read_and_split(path: str, delimiter: str) -> List[List[str]]:
    """
    Read and split a file into a list of lists of strings
    To read allConflictSets.da, use delimiter = ' --- '.
    To read a configuration file, use delimiter = ' '.
    :param path: path to the file
    :param delimiter: delimiter to split the line
    :return: a list of lists of strings
    """
    lines = read_text_file(path)

    all_lines = []
    for line in lines:
        elements = line.strip().split(delimiter)

        all_lines.append(elements)

    return all_lines


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
