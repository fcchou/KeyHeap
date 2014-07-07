from key_heap import KeyHeap

data_list = [('c', 3), ('a', 10), ('b', -2)]
data_dict = {'a': 10, 'b': -2, 'c': 3}


def pop(heap):
    while heap:
        yield heap.popitem()


def test_popitem():
    heap1 = KeyHeap()
    heap2 = KeyHeap()
    heap3 = KeyHeap()
    heap1.update(data_list)
    heap2.update(data_dict)
    heap3['b'] = -2
    heap3['a'] = 10
    heap3['c'] = 3

    expected = [('b', -2), ('c', 3), ('a', 10)]
    assert(expected == [i for i in pop(heap1)])
    assert(expected == [i for i in pop(heap2)])
    assert(expected == [i for i in pop(heap3)])


def test_maxheap():
    heap = KeyHeap(max_heap=True)
    heap.update(data_list)
    expected = [('a', 10), ('c', 3), ('b', -2)]
    assert(expected == [i for i in pop(heap)])


def test_peek():
    heap = KeyHeap()
    heap.update(data_list)
    assert(heap.peek() == heap.popitem())


def test_key_update():
    heap = KeyHeap()
    heap.update(data_list)
    assert(heap.peek() == ('b', -2))
    heap['b'] = 9
    assert(heap.peek() == ('c', 3))
    heap['a'] = -9
    assert(heap.peek() == ('a', -9))
