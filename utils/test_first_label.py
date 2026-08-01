
def test_first_label():
    """Test the functionality of the first_label argument."""
    T1 = nx.path_graph(3)
    T2 = nx.path_graph(2)
    actual = nx.join_trees([(T1, 0), (T2, 0)], first_label=10)
    expected_nodes = set(range(10, 16))
    assert set(actual.nodes()) == expected_nodes
    assert set(actual.neighbors(10)) == {11, 14}

