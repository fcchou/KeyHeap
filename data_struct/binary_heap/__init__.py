from collections import MutableMapping, Sequence
from _util import down_heap, up_heap


class KeyHeap(MutableMapping):
    """A heap data structure supporting key look-up and update.

    This is a binary heap that keep tracks of the keys of the input values.
    The heap is organized with the values, and one can use the key to quickly
    access and update the values associated with the keys. This is
    particularly useful for implementing Dijkstra's algorithm or Minimum
    spanning tree. KeyHeap is a subclass of collections.MutableMapping, having
    an interface mostly the same as Python built-in dict.

    Usage:
    >>> heap = KeyHeap(max_heap=True)  # create empty max-heap
    >>> heap = KeyHeap()  # create empty min-heap
    >>> heap['a'] = 1  # insert key-value into the heap
    >>> heap.update((("b", 10), ("c", 3)))  # insert multiple key-values
    >>> heap.peek()  # Get the current top element
    ('a', 1)
    >>> heap.pop()  # pop and return the current top element
    ('a', 1)
    >>> heap.peek()  # Get the current top element
    ('c', 3)
    >>> heap["b"] = 2  # Update the key value (cause heap reorganization)
    >>> heap.peek()  # Get the current top element
    ('b', 2)
    """

    def __init__(self, init_data=None, max_heap=False):
        """Create a heap. Default it returns a min-heap. Use
        'max_heap' keyword to get max-heap.

        Args:
            init_data - Optional, initiate the heap with input data. Must be
                        a dict or an iterable that returns (key, value).
            max_heap - True if being max-heap. Default to False.
        """
        self._key2idx = {}
        self._val_keys = []
        self._is_min_heap = not max_heap
        if init_data is not None:
            self.update(init_data)

    def __contains__(self, key):
        """Check if container has key."""
        return key in self._key2idx

    def __iter__(self):
        """Return a iterable of the keys."""
        return iter(self._key2idx)

    def __len__(self):
        """Return length of the container."""
        return len(self._val_keys)

    def __repr__(self):
        """Representation of the container."""
        repr_list = ['<KeyHeap ']
        if self:
            for val, key in self._val_keys:
                repr_list.append('{}: {}, '.format(repr(key), repr(val)))
            repr_list[-1] = repr_list[-1][:-2]
        repr_list.append('}>')
        return ''.join(repr_list)

    def __getitem__(self, key):
        """Return value from key."""
        if key not in self:
            raise KeyError("key not in container")
        idx = self._key2idx[key]
        return self._idx2val(idx)

    def __setitem__(self, key, value):
        """Set value of the key. If key does not in container, add the
        key-value into container. Otherwise update the value of the key.

        The update of key value uses the heap decrease/increase
        key algorithm.
        """
        if key not in self:
            self._val_keys.append((value, key))
            idx = len(self) - 1
            self._key2idx[key] = idx
            up_heap(self, idx)
        else:
            idx = self._key2idx[key]
            val_old = self._idx2val(idx)
            if val_old == value:
                return
            self._val_keys[idx] = (value, key)
            if self._upper_eq(value, val_old):
                up_heap(self, idx)
            else:
                down_heap(self, idx)

    def __delitem__(self, key):
        """Remove the key and its value from the container."""
        if key not in self:
            raise KeyError("key not in container")

        last_idx = len(self) - 1
        idx_curr = self._key2idx[key]
        self._swap(idx_curr, last_idx)
        del self._key2idx[key]
        self._val_keys.pop()
        if self:
            down_heap(self, idx_curr)

    def clear(self):
        """Empty the container."""
        self._key2idx.clear()
        self._val_keys = []

    def update(self, *args, **kwds):
        """D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E present and has a .keys() method, does: for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
        In either case, this is followed by: for k in F: D[k] = F[k]

        Use the heapify algorithm to rebuild the heap, to achieve O(n)
        performance for heap creation/merge.
        """
        def add(key, val):
            if key in self:
                idx = self._key2idx[key]
                self._val_keys[idx] = (val, key)
            else:
                self._key2idx[key] = len(self)
                self._val_keys.append((val, key))

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
            down_heap(self, idx)

    def pop(self, key=None):
        """Remove and return the given key and value.
        If key i not given, pop top element of the heap
        (min elementin min-heap; max element in max-heap).
        """
        if not self:
            raise KeyError("peek/pop from an empty container")
        if key is not None:
            return super(KeyHeap, self).pop(key)
        key, val = self.peek()
        del self[key]
        return key, val

    def peek(self):
        """Return the top element of the heap
        (min elementin min-heap; max element in max-heap).
        """
        if not self:
            raise KeyError("peek/pop from an empty container")
        val, key = self._val_keys[0]
        return key, val

    def copy(self):
        """Return a shallow copy of the container."""
        new = KeyHeap()
        new._key2idx = self._key2idx.copy()
        new._val_keys = self._val_keys[:]
        new._is_min_heap = self._is_min_heap
        return new

    def _idx2val(self, idx):
        """Return the value stored at position `idx` in heap."""
        return self._val_keys[idx][0]

    def _upper_eq(self, i, j):
        """Return True if i is upper than or equal to j.
        For min-heap, upper=less; for max-heap upper=greater.
        """
        if self._is_min_heap:
            return i <= j
        return i >= j

    def _swap(self, i1, i2):
        """Swap the values in two indices."""
        val1, key1 = self._val_keys[i1]
        val2, key2 = self._val_keys[i2]
        self._key2idx[key1], self._key2idx[key2] = i2, i1
        self._val_keys[i1] = val2, key2
        self._val_keys[i2] = val1, key1


class Heap(Sequence):
    """A basic heap data structure.

    This is a binary heap. Heap is a subclass of collections.Sequence, having
    an interface similar as Python built-in list.

    Usage:
    >>> heap = Heap(max_heap=True)  # create empty max-heap
    >>> heap = Heap()  # create empty min-heap
    >>> heap.push(10)  # insert value into the heap
    >>> heap.extend([0, 7]) # insert values from iterable
    >>> heap.peek()  # Get the current top element
    0
    >>> heap.pop()  # pop and return the current top element
    0
    >>> heap.peek()  # Get the current top element
    7
    """

    def __init__(self, init_data=None, max_heap=False):
        """Create a heap. Default it returns a min-heap. Use
        'max_heap' keyword to get max-heap.

        Args:
            init_data - Optional input iterable to populate the heap.
            max_heap - True if being max-heap. Default to False.
        """
        self._vals = []
        self._is_min_heap = not max_heap
        if init_data is not None:
            self.extend(init_data)

    def __contains__(self, value):
        """Check if container has value."""
        return value in self._vals

    def __iter__(self):
        """Return a iterable of the values."""
        return iter(self._vals)

    def __len__(self):
        """Return length of the container."""
        return len(self._vals)

    def __repr__(self):
        """Representation of the container."""
        return '<Heap ' + repr(self._vals) + '>'

    def __getitem__(self, index):
        """Return value from index."""
        if index >= len(self):
            raise IndexError("index out of range")
        return self._vals[index]

    def clear(self):
        """Empty the container."""
        self._vals = []

    def copy(self):
        """Return a shallow copy."""
        new = Heap()
        new._vals = self._vals[:]
        new._is_min_heap = self._is_min_heap
        return new

    def pop(self):
        """Remove and return the top element of the heap
        (min element in min-heap; max element in max-heap).
        """
        if not self:
            raise IndexError("peek/pop from an empty container")
        top_val = self.peek()
        last_idx = len(self) - 1
        self._swap(0, last_idx)
        self._vals.pop()
        if self:
            down_heap(self, 0)
        return top_val

    def peek(self):
        """Return the top element of the heap
        (min elementin min-heap; max element in max-heap).
        """
        if not self:
            raise IndexError("peek/pop from an empty container")
        return self[0]

    def push(self, value):
        """Add a value into the heap."""
        self._vals.append(value)
        idx = len(self) - 1
        up_heap(self, idx)

    def poppush(self, value):
        """Pop from the heap then push value into the heap.
        More efficient then pop() followed by push().
        """
        top_val = self.peek()
        self._vals[0] = value
        down_heap(self, 0)
        return top_val

    def pushpop(self, value):
        """Push value into the heap then pop from the heap.
        More efficient then push() followed by pop().
        """
        top_val = self.peek()
        if self._upper_eq(value, top_val):
            return value
        self._vals[0] = value
        down_heap(self, 0)
        return top_val

    def extend(self, iterable):
        """Add values to the heap from an iterable.

        Use the heapify algorithm to rebuild the heap, to achieve O(n)
        performance for heap creation/merge.
        """
        self._vals.extend(iterable)
        len_half = len(self) // 2
        for idx in reversed(xrange(len_half)):
            down_heap(self, idx)

    def _idx2val(self, idx):
        """Return the value stored at position `idx` in heap."""
        return self[idx]

    def _upper_eq(self, i, j):
        """Return True if i is upper than or equal to j.
        For min-heap, upper=less; for max-heap upper=greater.
        """
        if self._is_min_heap:
            return i <= j
        return i >= j

    def _swap(self, i1, i2):
        """Swap the values in two indices."""
        self._vals[i1], self._vals[i2] = self[i2], self[i1]
