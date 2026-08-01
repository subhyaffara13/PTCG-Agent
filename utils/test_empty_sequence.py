
def test_empty_sequence():
    assert Product(x*y, (x, -oo, oo), (y, 1, 0)).doit() == 1
    assert Product(x*y, (y, 1, 0), (x, -oo, oo)).doit() == 1
    assert Sum(x, (x, -oo, oo), (y, 1, 0)).doit() == 0
    assert Sum(x, (y, 1, 0), (x, -oo, oo)).doit() == 0


def test_empty_sequence():
    """Joining the empty sequence results in the tree with one node."""
    T = nx.join_trees([])
    assert len(T) == 1
    assert T.number_of_edges() == 0

