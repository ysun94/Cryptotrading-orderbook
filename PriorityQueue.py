import heapq

class PriorityQueue(object):

    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        heapq.heappop(self.heap)

    def isEmpty(self):
        if (not self.heap):
            return True
        else:
            return False

    def top(self):
        if (not self.isEmpty()):
            return self.heap[0]
