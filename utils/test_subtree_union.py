
def test_subtree_union():
    # See https://github.com/networkx/networkx/pull/3224
    # (35db1b551ee65780794a357794f521d8768d5049).
    # Test if subtree unions hare handled correctly by to_sets().
    uf = nx.utils.UnionFind()
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(4, 5)
    uf.union(1, 5)
    assert list(uf.to_sets()) == [{1, 2, 3, 4, 5}]

