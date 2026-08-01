
def test_trivial_rooted_tree_isomorphism():
    t1 = nx.Graph()
    t1.add_node("a")

    t2 = nx.Graph()
    t2.add_node("n")

    assert nx.isomorphism.rooted_tree_isomorphism(t1, "a", t2, "n") == [("a", "n")]

