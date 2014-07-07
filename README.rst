KeyHeap README
##############

A heap data structure supporting key look-up.

This is a binary heap that keep tracks of the keys of the input values.
The heap is organized with the values, and one can use the key to quickly
access and update the values associated with the keys. This is
particularly useful for implementing Dijkstra's algorithm or Minimum
spanning tree. KeyHeap is a subclss of collections.MutableMapping, having
an interface mostly the same as Python builtin dict.

Usage::

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

To test the code, run::
    $ nosetests
