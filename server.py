from multiprocessing.managers import BaseManager
from queue import Queue


class QueueManager(BaseManager):
    pass


input_queue = Queue()
output_queue = Queue()
QueueManager.register('get_input_queue', callable=lambda: input_queue)
QueueManager.register('get_output_queue', callable=lambda: output_queue)
m = QueueManager(address=('127.0.0.1', 50000), authkey=b'abracadabra')
s = m.get_server()
s.serve_forever()
