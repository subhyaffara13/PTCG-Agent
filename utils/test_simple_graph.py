
def test_simple_graph(method):
    # This graph looks as follows:
    #     (0) --5--> (1)
    graph = csr_array([[0, 5], [0, 0]])
    res = maximum_flow(graph, 0, 1, method=method)
    assert res.flow_value == 5
    expected_flow = np.array([[0, 5], [-5, 0]])
    assert_array_equal(res.flow.toarray(), expected_flow)

