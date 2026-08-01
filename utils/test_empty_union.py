
def test_empty_union():
    # Tests if a null-union does nothing.
    uf = nx.utils.UnionFind((0, 1))
    uf.union()
    assert uf[0] == 0
    assert uf[1] == 1


def test_empty_union():
    with pytest.raises(ValueError):
        nx.union_all([])

