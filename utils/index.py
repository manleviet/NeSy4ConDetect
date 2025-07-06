"""
MIGRATED to conflict-diagnosis-learning-benchmark repository
"""

import pickle
from typing import Dict


def read_index(path: str) -> Dict[str, int]:
    """
    Read the index file using pickle
    The index file is a dictionary with key as the feature name and value as the feature index
    :param path: path to the index file
    :return: a dictionary
    """
    with open(path, 'rb') as f:
        index = pickle.load(f)

    return index


def print_index_dictionary(dictionary: Dict[str, int]) -> None:
    """
    Print the dictionary with key as the feature name and value as the feature index
    :param dictionary: a dictionary
    :return: None
    """
    for key, value in dictionary.items():
        print(f'{key}: {value}')
