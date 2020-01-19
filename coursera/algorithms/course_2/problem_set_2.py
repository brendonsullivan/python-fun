"""
Problem set 2 of coursera algo2 pset.

Has class for doing min heap
Imports vertex and graph classes from problem set 1
"""
from problem_set_1 import Graph, Vertex, load_file


class minHeap:
    """Implements min heap data structure.

    Use min_value() to get the lowest value
    Use extract_min_key() to pop the key with the min value
    """

    def __init__(self, items):
        """Initialize heap from key value map of items."""
        self.values = items
        self.heap = [item for item in items.keys()]
        self.item_ids = {}
        self._build_heap()

    def _left_child_id(self, id):
        left_id = id * 2 + 1
        if left_id >= len(self.heap):
            left_id = None
        return left_id

    def _right_child_id(self, id):
        right_id = id * 2 + 2
        if right_id >= len(self.heap):
            right_id = None
        return right_id

    def _parent_id(self, id):
        parent = int((id - 1) / 2)
        if id == 0:
            parent = None
        return parent

    def _swap_items(self, id1, id2):
        temp = self.heap[id1]
        self.heap[id1] = self.heap[id2]
        self.heap[id2] = temp

        # updating reverse index
        self.item_ids[self.heap[id1]] = id1
        self.item_ids[self.heap[id2]] = id2

    def _heapify(self, id):
        smallestid = id
        smallest_val = self.values[self.heap[id]]
        leftid = self._left_child_id(id)
        rightid = self._right_child_id(id)

        if leftid is not None:
            left_val = self.values[self.heap[leftid]]
            if left_val < smallest_val:
                smallestid = leftid
                smallest_val = left_val

        if rightid is not None:
            right_val = self.values[self.heap[rightid]]
            if right_val < smallest_val:
                smallestid = rightid
                smallest_val = right_val

        if smallestid == id:
            return
        else:
            self._swap_items(id, smallestid)
            self._heapify(smallestid)

    def _build_heap(self):
        heap_size = len(self.heap)
        for offset in range(0, int(heap_size/2)+1):
            current_id = int(heap_size / 2) - offset
            self._heapify(current_id)

        # creating reverse index
        for id in range(len(self.heap)):
            key = self.heap[id]
            self.item_ids[key] = id

    def _bubble_up(self, id, value):
        while(True):
            parent_id = self._parent_id(id)
            if parent_id is None:
                break
            elif self.values[self.heap[parent_id]] < value:
                break
            else:
                self._swap_items(id, parent_id)
                id = parent_id

    def min_value(self):
        """Get the minimum value."""
        return self.values[self.heap[0]]

    def extract_min_key(self):
        """Pop the key with the minimal value from the heap.

        Returns key, value
        """
        assert len(self.heap) > 0, "No items in the heap"
        right_most_leaf = len(self.heap) - 1
        self._swap_items(right_most_leaf, 0)
        min_key = self.heap.pop()
        min_val = self.values.pop(min_key)
        if len(self.heap) > 0:
            self._heapify(0)

        return min_key, min_val

    def update_value(self, key, new_val):
        """Update value for given key."""
        self.values[key] = new_val
        self._build_heap()

    def decrease_value(self, key, new_val):
        """Update a current value with a lower value."""
        assert self.values[key] > new_val, "new value is not lower"
        self.values[key] = new_val

        key_id = self.item_ids[key]
        self._bubble_up(key_id, new_val)

    def insert(self, key, value):
        """Add a new key + value to the heap."""
        self.values[key] = value
        self.heap.append(key)
        self.item_ids[key] = len(self.heap) - 1

        key_id = len(self.heap) - 1
        self._bubble_up(key_id, value)

class Dijkstra(Graph):
    
