
def test_from_numpy_array_nodelist_rountrip(graph, nodes):
    G = graph(5)
    A = nx.to_numpy_array(G)
    expected = nx.relabel_nodes(G, mapping=dict(enumerate(nodes)), copy=True)
    H = nx.from_numpy_array(A, edge_attr=None, nodelist=nodes)
    assert graphs_equal(H, expected)

    # With an isolated node
    G = graph(4)
    G.add_node("foo")
    A = nx.to_numpy_array(G)
    expected = nx.relabel_nodes(G, mapping=dict(zip(G.nodes, nodes)), copy=True)
    H = nx.from_numpy_array(A, edge_attr=None, nodelist=nodes)
    assert graphs_equal(H, expected)

