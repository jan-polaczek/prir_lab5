from multiprocessing.managers import BaseManager
from time import time
import sys


class QueueManager(BaseManager):
    pass


def read(filename):
    with open(filename, 'r') as f:
        row_count, _ = [int(el) for el in f.readline().split()]
        arr = []
        for i in range(row_count):
            arr.append([float(el) for el in f.readline().split()])
    return arr


def divide_tasks(matrix, vector):
    tasks = []
    for i in range(len(matrix)):
        tasks.append({
            'matrix_row': matrix[i],
            'vector': vector,
            'idx': i
        })
    return tasks


if __name__ == '__main__':
    start_time = time()
    QueueManager.register('get_input_queue')
    QueueManager.register('get_output_queue')
    m = QueueManager(address=('192.168.0.100', 50000), authkey=b'abracadabra')
    m.connect()
    input_queue = m.get_input_queue()
    output_queue = m.get_output_queue()

    matrix_filename = sys.argv[1] if len(sys.argv) > 1 else "A.dat"
    vector_filename = sys.argv[2] if len(sys.argv) > 2 else "X.dat"

    matrix = read(matrix_filename)
    vector = read(vector_filename)

    tasks = divide_tasks(matrix, vector)
    task_count = len(tasks)

    input_queue.put(tasks)
    result = [0 for i in range(task_count)]
    calculation_start_time = time()
    for i in range(task_count):
        partial_result = output_queue.get()
        result[partial_result['idx']] = partial_result['value']
    print(f'Calculation time: {time() - calculation_start_time} seconds.')
    with open('out.dat', 'w') as f:
        for i in range(task_count):
            f.write(f'{result[i]}\n')
    print(f'Execution time: {time() - start_time} seconds.')

