
def test_implementations_consistent(strings):
    """Ensure results are consistent between prefix_tree implementations."""
    assert graphs_equal(nx.prefix_tree(strings), nx.prefix_tree_recursive(strings))

