
def test_rooted_tree_isomorphism_different_order():
    t1 = nx.Graph([("a", "b"), ("a", "c")])
    t2 = nx.Graph([("a", "b")])
    assert nx.isomorphism.tree_isomorphism(t1, t2) == []

