from binary_heap import KeyHeap, Heap

num_list = [3, 10, -2]
keyval_list = [('c', 3), ('a', 10), ('b', -2)]
keyval_dict = {'a': 10, 'b': -2, 'c': 3}


def pop_heap(heap):
    while heap:
        yield heap.pop()


# --- Heap Tests ---
def test_pop_heap():
    heap1 = Heap(num_list)
    heap2 = Heap()
    heap3 = Heap()
    heap2.extend(num_list)
    for i in num_list:
        heap3.push(i)

    expected = [-2, 3, 10]
    assert(expected == [i for i in pop_heap(heap1)])
    assert(expected == [i for i in pop_heap(heap2)])
    assert(expected == [i for i in pop_heap(heap3)])


def test_max_heap():
    heap = Heap(num_list, max_heap=True)
    expected = [10, 3, -2]
    assert(expected == [i for i in pop_heap(heap)])


def test_peek_heap():
    heap = Heap(num_list)
    assert(heap.peek() == heap.pop())


def test_push_pop():
    heap = Heap(num_list)
    assert(heap.pushpop(0) == -2)
    assert(heap.pushpop(-1) == -1)
    assert(heap.poppush(99) == 0)
    assert(heap.poppush(-10) == 3)


def test_copy_heap():
    heap = Heap(num_list)
    copy = heap.copy()
    assert(heap._vals == copy._vals)
    assert(heap is not copy)


def test_clear_heap():
    heap = Heap(num_list)
    assert(len(heap) == 3)
    heap.clear()
    assert(len(heap) == 0)
    assert(not heap)


# --- KeyHeap Tests ---
def test_pop_keyheap():
    heap1 = KeyHeap(keyval_list)
    heap2 = KeyHeap()
    heap3 = KeyHeap()
    heap2.update(keyval_dict)
    heap3['b'] = -2
    heap3['a'] = 10
    heap3['c'] = 3

    expected = [('b', -2), ('c', 3), ('a', 10)]
    assert(expected == [i for i in pop_heap(heap1)])
    assert(expected == [i for i in pop_heap(heap2)])
    assert(expected == [i for i in pop_heap(heap3)])


def test_max_keyheap():
    heap = KeyHeap(keyval_dict, max_heap=True)
    expected = [('a', 10), ('c', 3), ('b', -2)]
    assert(expected == [i for i in pop_heap(heap)])


def test_peek_keyheap():
    heap = KeyHeap(keyval_list)
    assert(heap.peek() == heap.pop())


def test_key_update():
    heap = KeyHeap(keyval_list)
    assert(heap.peek() == ('b', -2))
    heap['b'] = 9
    assert(heap.peek() == ('c', 3))
    heap['a'] = -9
    assert(heap.peek() == ('a', -9))


def test_copy_keyheap():
    heap = KeyHeap(keyval_list)
    copy = heap.copy()
    assert(heap._val_keys == copy._val_keys)
    assert(heap._key2idx == copy._key2idx)
    assert(heap is not copy)


def test_clear_keyheap():
    heap = KeyHeap(keyval_list)
    assert(len(heap) == 3)
    heap.clear()
    assert(len(heap) == 0)
    assert(not heap)
