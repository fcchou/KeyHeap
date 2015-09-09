README
######

This is a collection of useful data structures missing in Python standard
library. All codes are implemented in pure python. To test the code, simply
use nose::
    $ nosetests

Binary Heap
===========

Heap
----
Basic heap supporting push(), pop(), and heapify (use extend()). Default
is min-heap, but max-heap can be enabled by passing `max_heap=True` keyword
during initialization.

This is a binary heap. Heap is a subclass of collections.Sequence, having
an interface similar as Python built-in list.

Usage::

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

KeyHeap
-------
A heap data structure supporting key look-up and update.

This is a binary heap that keep tracks of the keys of the input values.
The heap is organized with the values, and one can use the key to quickly
access and update the values associated with the keys. This is
particularly useful for implementing Dijkstra's algorithm or Minimum
spanning tree. KeyHeap is a subclass of collections.MutableMapping, having
an interface mostly the same as Python built-in dict.

Usage::

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

Union Find
==========
A union find data structure.

The data structure is implemented with union-by-rank and path compression
to achieve almost constant runtime. The interface is similar to a Python
set. All values in the container must be unique.

Usage::

    >>> uf = UnionFind(10)  # Initialize with 10 elements (0-9)
    >>> uf.n_subset  # Each element is in its own subset initially
    10
    >>> uf.union(1, 5)  # Join subsets containing 1 and 5
    >>> uf.find(1) == uf.find(5)  # 1 and 5 are in the same subset
    True
    >>> uf.find(1) == uf.find(2)  # 1 and 2 are in different subset
    False
    >>> uf.n_subset  # After one union, n_subset decrease by 1
    9
