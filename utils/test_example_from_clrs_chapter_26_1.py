
def test_example_from_clrs_chapter_26_1(method):
    # See page 659 in CLRS second edition, but note that the maximum flow
    # we find is slightly different than the one in CLRS; we push a flow of
    # 12 to v_1 instead of v_2.
    graph = csr_array([[0, 16, 13, 0, 0, 0],
                       [0, 0, 10, 12, 0, 0],
                       [0, 4, 0, 0, 14, 0],
                       [0, 0, 9, 0, 0, 20],
                       [0, 0, 0, 7, 0, 4],
                       [0, 0, 0, 0, 0, 0]])
    res = maximum_flow(graph, 0, 5, method=method)
    assert res.flow_value == 23
    expected_flow = np.array([[0, 12, 11, 0, 0, 0],
                              [-12, 0, 0, 12, 0, 0],
                              [-11, 0, 0, 0, 11, 0],
                              [0, -12, 0, 0, -7, 19],
                              [0, 0, -11, 7, 0, 4],
                              [0, 0, 0, -19, -4, 0]])
    assert_array_equal(res.flow.toarray(), expected_flow)

