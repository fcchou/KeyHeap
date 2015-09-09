from union_find import UnionFind

letter_data = ['a', 'b', 'c']


def test_init():
    uf = UnionFind(3)
    uf.add(('a', 1))
    for i in xrange(3):
        assert(i in uf)
    assert(('a', 1) in uf)

    uf = UnionFind(letter_data)
    for i in letter_data:
        assert(i in uf)
    assert(1 not in uf)

    uf = uf.copy()
    uf = UnionFind(letter_data)
    for i in letter_data:
        assert(i in uf)


def test_union_find():
    uf = UnionFind(5)
    assert(uf.find(0) != uf.find(1))
    assert(uf.find(0) == uf.find(0))
    assert(uf.find(0) != uf.find(2))
    assert(uf.n_subset == 5)

    uf.union(1, 0)
    assert(uf.is_same_subset(0, 1))
    assert(not uf.is_same_subset(0, 2))
    assert(uf.n_subset == 4)

    uf.union(2, 4)
    subsets = uf.get_subsets()
    expected_subsets = [{0, 1}, {2, 4}, {3}]
    assert(len(subsets) == len(expected_subsets))
    for i in expected_subsets:
        assert(i in subsets)

    uf.union(2, 3)
    uf.union(3, 4)
    uf.union(0, 4)
    assert(uf.find(1) == uf.find(3))
    assert(uf.n_subset == 1)
