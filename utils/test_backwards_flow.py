
def test_backwards_flow(method):
    # This example causes backwards flow between vertices 3 and 4,
    # and so this test ensures that we handle that accordingly. See
    #     https://stackoverflow.com/q/38843963/5085211
    # for more information.
    graph = csr_array([[0, 10, 0, 0, 10, 0, 0, 0],
                       [0, 0, 10, 0, 0, 0, 0, 0],
                       [0, 0, 0, 10, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 10],
                       [0, 0, 0, 10, 0, 10, 0, 0],
                       [0, 0, 0, 0, 0, 0, 10, 0],
                       [0, 0, 0, 0, 0, 0, 0, 10],
                       [0, 0, 0, 0, 0, 0, 0, 0]])
    res = maximum_flow(graph, 0, 7, method=method)
    assert res.flow_value == 20
    expected_flow = np.array([[0, 10, 0, 0, 10, 0, 0, 0],
                              [-10, 0, 10, 0, 0, 0, 0, 0],
                              [0, -10, 0, 10, 0, 0, 0, 0],
                              [0, 0, -10, 0, 0, 0, 0, 10],
                              [-10, 0, 0, 0, 0, 10, 0, 0],
                              [0, 0, 0, 0, -10, 0, 10, 0],
                              [0, 0, 0, 0, 0, -10, 0, 10],
                              [0, 0, 0, -10, 0, 0, -10, 0]])
    assert_array_equal(res.flow.toarray(), expected_flow)

