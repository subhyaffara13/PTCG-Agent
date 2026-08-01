
def test_bottle_neck_graph(method):
    # This graph cannot use the full capacity between 0 and 1:
    #     (0) --5--> (1) --3--> (2)
    graph = csr_array([[0, 5, 0], [0, 0, 3], [0, 0, 0]])
    res = maximum_flow(graph, 0, 2, method=method)
    assert res.flow_value == 3
    expected_flow = np.array([[0, 3, 0], [-3, 0, 3], [0, -3, 0]])
    assert_array_equal(res.flow.toarray(), expected_flow)

