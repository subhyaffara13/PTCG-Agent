
def test_maximum_bipartite_matching_graph_that_causes_augmentation():
    # In this graph, column 1 is initially assigned to row 1, but it should be
    # reassigned to make room for row 2.
    graph = csr_array([[1, 1], [1, 0]])
    x = maximum_bipartite_matching(graph, perm_type='column')
    y = maximum_bipartite_matching(graph, perm_type='row')
    expected_matching = np.array([1, 0])
    assert_array_equal(expected_matching, x)
    assert_array_equal(expected_matching, y)

