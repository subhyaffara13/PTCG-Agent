
def test_cache_dict_get_set_state(graph):
    G = nx.path_graph(5, graph())
    G.nodes, G.edges, G.adj, G.degree
    if G.is_directed():
        G.pred, G.succ, G.in_edges, G.out_edges, G.in_degree, G.out_degree
    cached_dict = G.__dict__
    assert "nodes" in cached_dict
    assert "edges" in cached_dict
    assert "adj" in cached_dict
    assert "degree" in cached_dict
    if G.is_directed():
        assert "pred" in cached_dict
        assert "succ" in cached_dict
        assert "in_edges" in cached_dict
        assert "out_edges" in cached_dict
        assert "in_degree" in cached_dict
        assert "out_degree" in cached_dict

    # Raises error if the cached properties and views do not work
    pickle.loads(pickle.dumps(G, -1))
    deepcopy(G)

