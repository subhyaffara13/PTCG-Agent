
def test_selfloops_removal_multi(graph_type):
    """test removing selfloops behavior vis-a-vis altering a dict while iterating.
    cf. gh-4068"""
    G = nx.complete_graph(3, create_using=graph_type)
    # Defaults - see gh-4080
    G.add_edge(0, 0)
    G.add_edge(0, 0)
    G.remove_edges_from(nx.selfloop_edges(G))
    assert (0, 0) not in G.edges()
    # With keys
    G.add_edge(0, 0)
    G.add_edge(0, 0)
    with pytest.raises(RuntimeError):
        G.remove_edges_from(nx.selfloop_edges(G, keys=True))
    # With data
    G.add_edge(0, 0)
    G.add_edge(0, 0)
    with pytest.raises(TypeError):
        G.remove_edges_from(nx.selfloop_edges(G, data=True))
    # With keys and data
    G.add_edge(0, 0)
    G.add_edge(0, 0)
    with pytest.raises(RuntimeError):
        G.remove_edges_from(nx.selfloop_edges(G, data=True, keys=True))

