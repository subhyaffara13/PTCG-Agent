
def test_disconnected_graph(method):
    # This tests the following disconnected graph:
    #     (0) --5--> (1)    (2) --3--> (3)
    graph = csr_array([[0, 5, 0, 0],
                       [0, 0, 0, 0],
                       [0, 0, 9, 3],
                       [0, 0, 0, 0]])
    res = maximum_flow(graph, 0, 3, method=method)
    assert res.flow_value == 0
    expected_flow = np.zeros((4, 4), dtype=np.int32)
    assert_array_equal(res.flow.toarray(), expected_flow)


def test_disconnected_graph():
    # https://github.com/networkx/networkx/issues/1144
    G = nx.Graph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4)])
    assert not nx.is_tree(G)

    G = nx.DiGraph()
    G.add_edges_from([(0, 1), (1, 2), (2, 0), (3, 4)])
    assert not nx.is_tree(G)


def test_disconnected_graph():
    G = nx.fast_gnp_random_graph(100, 0.01, seed=42)
    cuts = nx.all_node_cuts(G)
    pytest.raises(nx.NetworkXError, next, cuts)

