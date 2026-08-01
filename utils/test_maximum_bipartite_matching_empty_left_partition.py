
def test_maximum_bipartite_matching_empty_left_partition():
    graph = csr_array((2, 0))
    x = maximum_bipartite_matching(graph, perm_type='row')
    y = maximum_bipartite_matching(graph, perm_type='column')
    assert_array_equal(np.array([]), x)
    assert_array_equal(np.array([-1, -1]), y)

