from random import random

rows = 2000
columns = 1000

matrix = []
vector = []

for i in range(rows):
    row = [random() * 100 - 50 for j in range(columns)]
    matrix.append(row)

for i in range(columns):
    vector.append(random() * 100 - 50)

with open('A.dat', 'w') as f:
    f.write(f'{rows} {columns}\n')
    for row in matrix:
        f.write(' '.join(['%.2f' % el for el in row]))
        f.write('\n')

with open('X.dat', 'w') as f:
    f.write(f'{columns} 1\n')
    f.write('\n'.join(['%.2f' % el for el in vector]))
