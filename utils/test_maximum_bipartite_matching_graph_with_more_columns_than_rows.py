
def test_maximum_bipartite_matching_graph_with_more_columns_than_rows():
    graph = csr_array([[1, 1, 0], [0, 0, 1]])
    x = maximum_bipartite_matching(graph, perm_type='column')
    y = maximum_bipartite_matching(graph, perm_type='row')
    assert_array_equal(np.array([0, 2]), x)
    assert_array_equal(np.array([0, -1, 1]), y)

