import os

ROOT_PATH = '../../data/busybox'
folder = "%s/diagnosis/invalid_confs/txt/1" % ROOT_PATH

# read all files with filename starting "conf" in the folder
files = [f for f in os.listdir(folder) if f.startswith('conf')]

for file in files:
    old_lines = []
    new_lines = []
    with open(os.path.join(folder, file), 'r') as f:
        lines = f.readlines()
        for line in lines:
            stripped_line = line.strip()
            old_lines.append(stripped_line)
            # if stripped_line == "FEATURE_TOP_SMP_CPU true":
            #     print(f'Found line - {file} - {line}')
            if stripped_line in new_lines:
                continue
            new_lines.append(stripped_line)

    if len(old_lines) != len(new_lines):
        print(f'Duplicate lines found - {file} - {len(old_lines)} - {len(new_lines)}')

    # save new_lines to new file
    with open(os.path.join(folder, file), 'w') as f:
        for line in new_lines[:-1]:
            f.write(f"{line}\n")
        f.write(new_lines[-1])