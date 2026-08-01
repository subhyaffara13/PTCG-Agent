
def test_maximum_bipartite_matching_explicit_zeros_count_as_edges():
    data = [0, 0]
    indices = [1, 0]
    indptr = [0, 1, 2]
    graph = csr_array((data, indices, indptr), shape=(2, 2))
    x = maximum_bipartite_matching(graph, perm_type='row')
    y = maximum_bipartite_matching(graph, perm_type='column')
    expected_matching = np.array([1, 0])
    assert_array_equal(expected_matching, x)
    assert_array_equal(expected_matching, y)

