
def test_raises_graph_type(fn, graph_type):
    """Check that broadcast functions properly raise for directed and multigraph types."""
    G = nx.path_graph(5, create_using=graph_type)
    with pytest.raises(nx.NetworkXNotImplemented, match=r"not implemented for"):
        fn(G)

