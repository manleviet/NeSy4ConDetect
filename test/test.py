import csv

def read_conflicts_csv(file_path):
    with open(file_path, 'r') as file:
        print(f'Reading file: {file_path}')

        reader = csv.reader(file)
        rows = list(reader)
        num_rows = len(rows)
        num_columns = len(rows[0]) if rows else 0
        print(f'Number of rows: {num_rows}')
        print(f'Number of columns: {num_columns}')

        # loop through all rows
        # check 1 & -1 in each row
        # for index, row in enumerate(rows):
        #     if '1' in row or '-1' in row:
        #         if '0' in row:
        #             print(f'Row {index} has 1 or -1 and 0')
        #         else:
        #             print(f'Row {index} has 1 or -1')

# Usage
read_conflicts_csv('../data/busybox/126725/conflicts_126725.csv')
read_conflicts_csv('../data/busybox/126725/invalid_confs_126725.csv')