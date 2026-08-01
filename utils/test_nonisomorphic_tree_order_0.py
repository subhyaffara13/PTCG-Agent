
def test_nonisomorphic_tree_order_0():
    assert nx.number_of_nonisomorphic_trees(0) == 0
    assert list(nx.nonisomorphic_trees(0)) == []

