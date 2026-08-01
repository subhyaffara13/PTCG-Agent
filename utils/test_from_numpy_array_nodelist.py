
def test_from_numpy_array_nodelist(nodes):
    A = np.diag(np.ones(4), k=1)
    # Without edge attributes
    expected = nx.relabel_nodes(
        nx.path_graph(5), mapping=dict(enumerate(nodes)), copy=True
    )
    G = nx.from_numpy_array(A, edge_attr=None, nodelist=nodes)
    assert graphs_equal(G, expected)

    # With edge attributes
    nx.set_edge_attributes(expected, 1.0, name="weight")
    G = nx.from_numpy_array(A, nodelist=nodes)
    assert graphs_equal(G, expected)

