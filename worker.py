from multiprocessing import Process
from multiprocessing.managers import BaseManager
import sys
from math import ceil


class QueueManager(BaseManager):
    pass


REPS = 300


class Worker(Process):
    def __init__(self, output_queue, tasks):
        self.tasks = tasks
        self.output_queue = output_queue
        super(Worker, self).__init__()

    def run(self):
        for task in self.tasks:
            result = self.solve_task(task)
            self.output_queue.put(result)

    @staticmethod
    def solve_task(task):
        for i in range(REPS):
            idx = task['idx']
            matrix_row = task['matrix_row']
            vector = task['vector']
            result = {
                'idx': idx,
                'value': 0
            }
            for i in range(len(matrix_row)):
                result['value'] += matrix_row[i] * vector[i][0]
        return result


def distribute_tasks(tasks, cpu_count):
    distributed_tasks = []
    task_count = len(tasks)
    tasks_per_worker = ceil(task_count / cpu_count)
    i = 0
    while i < task_count:
        distributed_tasks.append(tasks[i:min(i+tasks_per_worker, task_count)])
        i += tasks_per_worker
    return distributed_tasks


if __name__ == '__main__':
    cpu_count = int(sys.argv[1]) if len(sys.argv) > 1 else 2

    QueueManager.register('get_input_queue')
    QueueManager.register('get_output_queue')
    m = QueueManager(address=('192.168.0.100', 50000), authkey=b'abracadabra')
    m.connect()
    input_queue = m.get_input_queue()
    output_queue = m.get_output_queue()

    tasks = input_queue.get()
    if len(tasks) < cpu_count:
        print(f'Total number of tasks is smaller than given cpu count. Setting cpu count to {len(tasks)}.')
        cpu_count = len(tasks)

    distributed_tasks = distribute_tasks(tasks, cpu_count)
    for task_set in distributed_tasks:
        w = Worker(output_queue, task_set)
        w.start()
