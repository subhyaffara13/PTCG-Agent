
def test_add_reverse_edges_large_graph(method):
    # Regression test for https://github.com/scipy/scipy/issues/14385
    n = 100_000
    indices = np.arange(1, n)
    indptr = np.array(list(range(n)) + [n - 1])
    data = np.ones(n - 1, dtype=np.int32)
    graph = csr_array((data, indices, indptr), shape=(n, n))
    res = maximum_flow(graph, 0, n - 1, method=method)
    assert res.flow_value == 1
    expected_flow = graph - graph.transpose()
    assert_array_equal(res.flow.data, expected_flow.data)
    assert_array_equal(res.flow.indices, expected_flow.indices)
    assert_array_equal(res.flow.indptr, expected_flow.indptr)

