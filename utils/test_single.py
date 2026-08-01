
def test_single():
    """Joining just one tree yields a tree with one more node."""
    T = nx.empty_graph(1)
    trees = [(T, 0)]
    actual_with_label = nx.join_trees(trees, label_attribute="custom_label")
    expected = nx.path_graph(2)
    assert nodes_equal(list(expected), list(actual_with_label))
    assert edges_equal(list(expected.edges()), list(actual_with_label.edges()))

