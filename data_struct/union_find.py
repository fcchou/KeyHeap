from collections import defaultdict
DEFAULT_ROOT = 0


class UnionFind(object):
    """A union find data structure.

    The data structure is implemented with union-by-rank and path compression
    to achieve almost constant runtime. The interface is similar to a Python
    set. All values in the container must be unique.

    Usage:
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

    """
    def __init__(self, init_data=None):
        """Create the UnionFind with init_data.

        Args:
            init_data - Can be a iterable for the elements to be added. Or an
                        integer, which adds range(init_data) into container.
        """

        if init_data is None:
            self._val2root = {}
            self._val2rank = {}
            self._n_subset = 0
            return

        if isinstance(init_data, int):
            init_data = xrange(init_data)
        self._val2root = {i: i for i in init_data}
        self._val2rank = {i: 0 for i in init_data}
        self._n_subset = len(self)

    def __len__(self):
        """Return length of the container."""
        return len(self._val2root)

    def __iter__(self):
        """Return iterator of the container."""
        return iter(self._val2root)

    def __contains__(self, value):
        """Check if value is in the container."""
        return value in self._val2root

    def __repr__(self):
        """Python repr string."""
        repr_list = ["<UnionFind {"]
        for i in self:
            repr_list.append('{}, '.format(repr(i)))
        repr_list[-1] = repr_list[-1][:-2]
        repr_list.append(["}>"])
        return ''.join(repr_list)

    @property
    def n_subset(self):
        """Current number of subsets."""
        return self._n_subset

    def clear(self):
        """Remove all elements."""
        self._val2root.clear()
        self._val2rank.clear()
        self._n_subset = 0

    def copy(self):
        """Return a shallow copy."""
        new = UnionFind()
        new._val2root = self._val2root.copy()
        new._val2rank = self._val2rank.copy()
        new._n_subset = self._n_subset
        return new

    def add(self, value):
        """Add a new value as a singleton. Won't do anything if value is
        already in container."""
        if value in self:
            return
        self._val2root[value] = value
        self._val2rank[value] = 0
        self._n_subset += 1

    def find(self, value):
        """Find the subset where the input value belongs to."""
        if value not in self:
            raise KeyError("value not in container")
        if self._n_subset == 1:
            # All in one set
            return DEFAULT_ROOT

        visited_keys = []
        while True:
            root = self._val2root[value]
            if root == value:
                break
            visited_keys.append(value)
            value = root

        # Path compression
        for key in visited_keys:
            self._val2root[key] = root
        return root

    def union(self, value1, value2):
        """Join the subsets where the two input values belong to."""
        if self.n_subset == 1:  # All in one set
            return
        root1 = self.find(value1)
        root2 = self.find(value2)
        if root1 == root2:
            return

        # Union by rank
        rank1 = self._val2rank[root1]
        rank2 = self._val2rank[root2]
        if rank1 > rank2:
            self._val2root[root2] = root1
        else:
            self._val2root[root1] = root2
            if rank1 == rank2:
                self._val2rank[root2] += 1
        self._n_subset -= 1

    def is_same_subset(self, value1, value2):
        """Check if two values are in the same subset."""
        return self.find(value1) == self.find(value2)

    def get_subsets(self):
        """Return the current subsets as a list of sets."""
        root2sets = defaultdict(set)
        for val in self:
            root = self.find(val)
            root2sets[root].add(val)
        return [subset for subset in root2sets.itervalues()]
