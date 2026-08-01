
def test_maximum_bipartite_matching_empty_graph():
    graph = csr_array((0, 0))
    x = maximum_bipartite_matching(graph, perm_type='row')
    y = maximum_bipartite_matching(graph, perm_type='column')
    expected_matching = np.array([])
    assert_array_equal(expected_matching, x)
    assert_array_equal(expected_matching, y)

