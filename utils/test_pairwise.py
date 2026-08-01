
def test_pairwise():
    nodes = range(4)
    node_pairs = [(0, 1), (1, 2), (2, 3)]
    node_pairs_cycle = node_pairs + [(3, 0)]
    assert list(pairwise(nodes)) == node_pairs
    assert list(pairwise(iter(nodes))) == node_pairs
    assert list(pairwise(nodes, cyclic=True)) == node_pairs_cycle
    empty_iter = iter(())
    assert list(pairwise(empty_iter)) == []
    empty_iter = iter(())
    assert list(pairwise(empty_iter, cyclic=True)) == []

