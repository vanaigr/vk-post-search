import os
import math
from collections import defaultdict

from_dir = 'posts'
to_dir = 'dedup'

if not os.path.exists(from_dir):
    raise RuntimeError("from_dir doesn't exist")

if not os.path.exists(to_dir):
    os.makedirs(to_dir)

files = os.listdir(from_dir)
files.sort()
fac = 100 / len(files)

seenNormalized = defaultdict(list) # by len
duplicates = 0
skipped = 0
prev_percent = -1

for i, file_name in enumerate(files):
    file_path = os.path.join(from_dir, file_name)

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    lines = content.split('\n')

    # убираем хештеги с обоих концов поста
    begin = 0
    end = 0
    for j in range(begin, len(lines)):
        if not lines[j].startswith('#'):
            lines[j] = lines[j].strip()
            if lines[j] == '':
                continue

            begin = j
            end = len(lines)
            for k in range(end-1, j, -1):
                lines[k] = lines[k].strip()
                if not lines[k].startswith('#') and lines[k] != '':
                    break
                end = k

            break

    normalized = ''.join(map(lambda l: l.strip(), lines[begin:end]))

    if normalized.endswith('\n'):
        raise RuntimeError('EOL at EOF:')

    if len(normalized) == 0:
        skipped = skipped + 1
        if skipped % 50 == 0:
            print(f'skipped {skipped}')
        continue

    cts = seenNormalized[len(normalized)]
    if normalized not in cts:
        cts.append(normalized)
        to_file_path = os.path.join(to_dir, file_name)
        with open(to_file_path, "w", encoding='utf-8') as file:
            file.write(content)
    else:
        duplicates = duplicates + 1

    percent = math.floor(i * fac)
    if percent != prev_percent:
        prev_percent = percent
        print(f'processed {i+1}, duplicates: {duplicates}')

print(f'done {len(files)}, duplicates: {duplicates}, skipped: {skipped}')
