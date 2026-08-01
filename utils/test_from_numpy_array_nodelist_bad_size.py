
def test_from_numpy_array_nodelist_bad_size():
    """An exception is raised when `len(nodelist) != A.shape[0]`."""
    n = 5  # Number of nodes
    A = np.diag(np.ones(n - 1), k=1)  # Adj. matrix for P_n
    expected = nx.path_graph(n)

    assert graphs_equal(nx.from_numpy_array(A, edge_attr=None), expected)
    nodes = list(range(n))
    assert graphs_equal(
        nx.from_numpy_array(A, edge_attr=None, nodelist=nodes), expected
    )

    # Too many node labels
    nodes = list(range(n + 1))
    with pytest.raises(ValueError, match="nodelist must have the same length as A"):
        nx.from_numpy_array(A, nodelist=nodes)

    # Too few node labels
    nodes = list(range(n - 1))
    with pytest.raises(ValueError, match="nodelist must have the same length as A"):
        nx.from_numpy_array(A, nodelist=nodes)

