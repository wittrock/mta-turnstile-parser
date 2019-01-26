import os

rows = []
for path in os.listdir('./data'):
    with open('./data/' + path, 'r') as f:
        # discard the first row of each file
        # XXX: they changed format on 10/18/14, parse that.
        rows.extend(f.readlines()[1:])

with open('./combined.csv', 'w+') as f:
    f.writelines(rows)
