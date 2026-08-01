
def test_numpy_multigraph(multigraph_test_graph, operator, expected):
    A = nx.to_numpy_array(multigraph_test_graph, multigraph_weight=operator)
    assert A[1, 0] == expected

