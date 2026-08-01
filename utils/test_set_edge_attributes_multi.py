
def test_set_edge_attributes_multi(graph_type):
    # Test single value
    G = nx.path_graph(3, create_using=graph_type)
    attr = "hello"
    vals = 3
    nx.set_edge_attributes(G, vals, attr)
    assert G[0][1][0][attr] == vals
    assert G[1][2][0][attr] == vals

    # Test multiple values
    G = nx.path_graph(3, create_using=graph_type)
    attr = "hi"
    edges = [(0, 1, 0), (1, 2, 0)]
    vals = dict(zip(edges, range(len(edges))))
    nx.set_edge_attributes(G, vals, attr)
    assert G[0][1][0][attr] == 0
    assert G[1][2][0][attr] == 1

    # Test dictionary of dictionaries
    G = nx.path_graph(3, create_using=graph_type)
    d = {"hi": 0, "hello": 200}
    edges = [(0, 1, 0)]
    vals = dict.fromkeys(edges, d)
    nx.set_edge_attributes(G, vals)
    assert G[0][1][0]["hi"] == 0
    assert G[0][1][0]["hello"] == 200
    assert G[1][2][0] == {}

