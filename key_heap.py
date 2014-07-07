from collections import MutableMapping
from itertools import izip


class KeyHeap(MutableMapping):
    """A heap data structure supporting key look-up and update.

    This is a binary heap that keep tracks of the keys of the input values.
    The heap is organized with the values, and one can use the key to quickly
    access and update the values associated with the keys. This is
    particularly useful for implementing Dijkstra's algorithm or Minimum
    spanning tree. KeyHeap is a subclss of collections.MutableMapping, having
    an interface mostly the same as Python builtin dict.

    Usage:
    >>> heap = KeyHeap(max_heap=True)  # create empty max-heap
    >>> heap = KeyHeap()  # create empty min-heap
    >>> heap['a'] = 1  # insert key-value into the heap
    >>> heap.update((("b", 10), ("c", 3)))  # insert multiple key-values
    >>> heap.peek()  # Get the current top element
    ('a', 1)
    >>> heap.popitem()  # pop and return the current top element
    ('a', 1)
    >>> heap.peek()  # Get the current top element
    ('c', 3)
    >>> heap["b"] = 2  # Update the key value (cause heap reorganization)
    >>> heap.peek()  # Get the current top element
    ('b', 2)
    """

    def __init__(self, max_heap=False):
        """Create an empty heap. Default it returns a min-heap. Use
        'max_heap' keyword to get max-heap.

        Args:
            max_heap - True if being max-heap. Default to False.
        """
        self._key2idx = {}
        self._idx2key = []
        self._vals = []
        self._is_min_heap = not max_heap

    def __contains__(self, key):
        """Check if container has key."""
        return key in self._key2idx

    def __iter__(self):
        """Return a iterable of the keys."""
        return iter(self._idx2key)

    def __len__(self):
        """Return length of the container."""
        return len(self._vals)

    def __repr__(self):
        """Representation of the container."""
        repr_list = ['<KeyHeap {']
        if self:
            for key, val in izip(self._idx2key, self._vals):
                repr_list.append('{}: {}, '.format(repr(key), repr(val)))
            repr_list[-1] = repr_list[-1][:-2]
        repr_list.append('}>')
        return ''.join(repr_list)

    def __getitem__(self, key):
        """Return value from key."""
        if key not in self:
            raise KeyError("cannot find key '{}'".format(key))
        idx = self._key2idx[key]
        return self._vals[idx]

    def __setitem__(self, key, value):
        """Set value of the key. If key does not in container, add the
        key-value into container. Otherwise update the value of the key.

        The update of key value uses the heap decrease/increase
        key algorithm.
        """
        if key not in self:
            self._insert(key, value)
        else:
            idx = self._key2idx[key]
            val_old = self._vals[idx]
            if val_old == value:
                return
            self._vals[idx] = value
            if self._upper_eq(value, val_old):
                self._up_heap(idx)
            else:
                self._down_heap(idx)

    def __delitem__(self, key):
        """Remove the key and its value from the container."""
        if key not in self:
            raise KeyError("cannot find key '{}'".format(key))
        last_idx = len(self) - 1
        idx_curr = self._key2idx[key]
        self._swap(idx_curr, last_idx)
        del self._key2idx[key]
        self._vals.pop()
        self._idx2key.pop()
        if self:
            self._down_heap(idx_curr)

    def clear(self):
        """Make the container empty."""
        self._key2idx.clear()
        self._idx2key = []
        self._vals = []

    def update(self, *args, **kwds):
        """D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E present and has a .keys() method, does: for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
        In either case, this is followed by: for k in F: D[k] = F[k]

        This uses the heapify algorithm to achieve O(n) performance for
        heap creation/merge.
        """
        def add(key, val):
            if key in self:
                idx = self._key2idx[key]
                self._vals[idx] = val
            else:
                self._key2idx[key] = len(self)
                self._idx2key.append(key)
                self._vals.append(val)

        def add_from_mapping(mapping):
            for key in mapping:
                val = mapping[key]
                add(key, val)

        def add_from_iterable(iterable):
            for key, val in iterable:
                add(key, val)

        for i, container in enumerate(args):
            try:
                if hasattr(container, "keys"):
                    add_from_mapping(container)
                else:
                    add_from_iterable(container)
            except Exception:
                raise TypeError(
                    "cannot convert update sequence element "
                    "#{} to a sequence".format(i))

        add_from_mapping(kwds)

        len_half = len(self) // 2
        for idx in reversed(xrange(len_half)):
            self._down_heap(idx)

    def popitem(self):
        """Remove and return the top element of the heap
        (min elementin min-heap; max element in max-heap).
        """
        if not self:
            raise KeyError("pop from an empty container")
        key, val = self.peek()
        del self[key]
        return key, val

    def peek(self):
        """Return the top element of the heap
        (min elementin min-heap; max element in max-heap).
        """
        if self:
            return self._idx2key[0], self._vals[0]
        return None

    def copy(self):
        """Return a shallow copy of the container."""
        new = self.__init__()
        new._key2idx = self._key2idx.copy()
        new._idx2key = self._idx2key[:]
        new._vals = self._vals[:]
        new._is_min_heap = self._is_min_heap
        return new

    def _upper_eq(self, i, j):
        """Return True if i is upper or equal to j. For min-heap,
        upper=less; for max-heap upper=greater.
        """
        if self._is_min_heap:
            return i <= j
        return i >= j

    def _get_parent(self, idx):
        """Get the parent index-value of the input index."""
        if idx == 0:
            return None, None
        idx_parent = (idx - 1) // 2
        val_parent = self._vals[idx_parent]
        return idx_parent, val_parent

    def _get_children(self, idx):
        """Get the children index-value of the input index."""
        length = len(self)
        idx_left = 2 * idx + 1
        if idx_left < length:
            val_left = self._vals[idx_left]
        else:
            idx_left = val_left = idx_right = val_right = None
            return idx_left, val_left, idx_right, val_right

        idx_right = idx_left + 1
        if idx_right < length:
            val_right = self._vals[idx_right]
        else:
            idx_right = val_right = None

        return idx_left, val_left, idx_right, val_right

    def _swap(self, i1, i2):
        """Swap the values in two indices."""
        key1, key2 = self._idx2key[i1], self._idx2key[i2]
        self._key2idx[key1], self._key2idx[key2] = i2, i1
        self._idx2key[i1], self._idx2key[i2] = key2, key1
        self._vals[i1], self._vals[i2] = self._vals[i2], self._vals[i1]

    def _down_heap(self, idx):
        """Perform down-heap operation on input index."""
        idx_curr = idx
        val_curr = self._vals[idx]
        while True:
            idx_left, val_left, idx_right, val_right = (
                self._get_children(idx_curr))
            if idx_left is None:
                break
            elif idx_right is None:
                child_idx_upper = idx_left
                child_val_upper = val_left
            else:
                if self._upper_eq(val_left, val_right):
                    child_idx_upper = idx_left
                    child_val_upper = val_left
                else:
                    child_idx_upper = idx_right
                    child_val_upper = val_right

            if self._upper_eq(val_curr, child_val_upper):
                break
            self._swap(idx_curr, child_idx_upper)
            idx_curr = child_idx_upper

    def _up_heap(self, idx):
        """Perform up-heap operation on input index."""
        idx_curr = idx
        val_curr = self._vals[idx]
        while True:
            idx_parent, val_parent = self._get_parent(idx_curr)
            if idx_parent is None or self._upper_eq(val_parent, val_curr):
                break
            self._swap(idx_curr, idx_parent)
            idx_curr = idx_parent

    def _insert(self, key, val):
        """Insert a new key-value into the heap container."""
        self._vals.append(val)
        idx = len(self) - 1
        self._key2idx[key] = idx
        self._idx2key.append(key)
        self._up_heap(idx)
