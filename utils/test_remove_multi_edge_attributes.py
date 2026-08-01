
def test_remove_multi_edge_attributes(graph_type):
    # Test removing single attribute
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    attr = "hello"
    vals = 100
    nx.set_edge_attributes(G, vals, attr)
    nx.remove_edge_attributes(G, attr)
    assert attr not in G[0][1][0]
    assert attr not in G[1][2][0]
    assert attr not in G[1][2][1]

    # Test removing only some attributes
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    other_attr = "other"
    other_vals = 200
    nx.set_edge_attributes(G, vals, attr)
    nx.set_edge_attributes(G, other_vals, other_attr)
    nx.remove_edge_attributes(G, attr)
    assert attr not in G[0][1][0]
    assert attr not in G[1][2][0]
    assert attr not in G[1][2][1]
    assert G[0][1][0][other_attr] == other_vals
    assert G[1][2][0][other_attr] == other_vals
    assert G[1][2][1][other_attr] == other_vals

    # Test removing multiple attributes
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    nx.set_edge_attributes(G, vals, attr)
    nx.set_edge_attributes(G, other_vals, other_attr)
    nx.remove_edge_attributes(G, attr, other_attr)
    assert attr not in G[0][1][0] and other_attr not in G[0][1][0]
    assert attr not in G[1][2][0] and other_attr not in G[1][2][0]
    assert attr not in G[1][2][1] and other_attr not in G[1][2][1]

    # Test removing multiple (not all) attributes
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    third_attr = "third"
    third_vals = 300
    nx.set_edge_attributes(
        G,
        {
            (u, v, k): {attr: vals, other_attr: other_vals, third_attr: third_vals}
            for u, v, k in G.edges(keys=True)
        },
    )
    nx.remove_edge_attributes(G, other_attr, third_attr)
    assert other_attr not in G[0][1][0] and third_attr not in G[0][1][0]
    assert other_attr not in G[1][2][0] and other_attr not in G[1][2][0]
    assert other_attr not in G[1][2][1] and other_attr not in G[1][2][1]
    assert G[0][1][0][attr] == vals
    assert G[1][2][0][attr] == vals
    assert G[1][2][1][attr] == vals

    # Test removing incomplete edge attributes
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    nx.set_edge_attributes(
        G,
        {
            (0, 1, 0): {attr: vals, other_attr: other_vals},
            (1, 2, 1): {attr: vals, other_attr: other_vals},
        },
    )
    nx.remove_edge_attributes(G, other_attr)
    assert other_attr not in G[0][1][0] and G[0][1][0][attr] == vals
    assert other_attr not in G[1][2][0]
    assert other_attr not in G[1][2][1]

    # Test removing subset of edge attributes
    G = nx.path_graph(3, create_using=graph_type)
    G.add_edge(1, 2)
    nx.set_edge_attributes(
        G,
        {
            (0, 1, 0): {attr: vals, other_attr: other_vals},
            (1, 2, 0): {attr: vals, other_attr: other_vals},
            (1, 2, 1): {attr: vals, other_attr: other_vals},
        },
    )
    nx.remove_edge_attributes(G, attr, ebunch=[(0, 1, 0), (1, 2, 0)])
    assert attr not in G[0][1][0] and other_attr in G[0][1][0]
    assert attr not in G[1][2][0] and other_attr in G[1][2][0]
    assert attr in G[1][2][1] and other_attr in G[1][2][1]

