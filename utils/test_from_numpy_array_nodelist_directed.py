
def test_from_numpy_array_nodelist_directed(nodes):
    A = np.diag(np.ones(4), k=1)
    # Without edge attributes
    H = nx.DiGraph([(0, 1), (1, 2), (2, 3), (3, 4)])
    expected = nx.relabel_nodes(H, mapping=dict(enumerate(nodes)), copy=True)
    G = nx.from_numpy_array(A, create_using=nx.DiGraph, edge_attr=None, nodelist=nodes)
    assert graphs_equal(G, expected)

    # With edge attributes
    nx.set_edge_attributes(expected, 1.0, name="weight")
    G = nx.from_numpy_array(A, create_using=nx.DiGraph, nodelist=nodes)
    assert graphs_equal(G, expected)

