
def test_maximum_bipartite_matching_empty_right_partition():
    graph = csr_array((0, 3))
    x = maximum_bipartite_matching(graph, perm_type='row')
    y = maximum_bipartite_matching(graph, perm_type='column')
    assert_array_equal(np.array([-1, -1, -1]), x)
    assert_array_equal(np.array([]), y)

