
def test_remove_edge_attributes(graph_type):
    # Test removing single attribute
    G = nx.path_graph(3, create_using=graph_type)
    attr = "hello"
    vals = 100
    nx.set_edge_attributes(G, vals, attr)
    nx.remove_edge_attributes(G, attr)
    assert len(nx.get_edge_attributes(G, attr)) == 0

    # Test removing only some attributes
    G = nx.path_graph(3, create_using=graph_type)
    other_attr = "other"
    other_vals = 200
    nx.set_edge_attributes(G, vals, attr)
    nx.set_edge_attributes(G, other_vals, other_attr)
    nx.remove_edge_attributes(G, attr)

    assert attr not in G[0][1]
    assert attr not in G[1][2]
    assert G[0][1][other_attr] == 200
    assert G[1][2][other_attr] == 200

    # Test removing multiple attributes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, vals, attr)
    nx.set_edge_attributes(G, other_vals, other_attr)
    nx.remove_edge_attributes(G, attr, other_attr)
    assert attr not in G[0][1] and other_attr not in G[0][1]
    assert attr not in G[1][2] and other_attr not in G[1][2]

    # Test removing multiple (not all) attributes
    G = nx.path_graph(3, create_using=graph_type)
    third_attr = "third"
    third_vals = 300
    nx.set_edge_attributes(
        G,
        {
            (u, v): {attr: vals, other_attr: other_vals, third_attr: third_vals}
            for u, v in G.edges()
        },
    )
    nx.remove_edge_attributes(G, other_attr, third_attr)
    assert other_attr not in G[0][1] and third_attr not in G[0][1]
    assert other_attr not in G[1][2] and third_attr not in G[1][2]
    assert G[0][1][attr] == vals
    assert G[1][2][attr] == vals

    # Test removing incomplete edge attributes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(G, {(0, 1): {attr: vals, other_attr: other_vals}})
    nx.remove_edge_attributes(G, other_attr)
    assert other_attr not in G[0][1] and G[0][1][attr] == vals
    assert other_attr not in G[1][2]

    # Test removing subset of edge attributes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_edge_attributes(
        G,
        {
            (u, v): {attr: vals, other_attr: other_vals, third_attr: third_vals}
            for u, v in G.edges()
        },
    )
    nx.remove_edge_attributes(G, other_attr, third_attr, ebunch=[(0, 1)])
    assert other_attr not in G[0][1] and third_attr not in G[0][1]
    assert other_attr in G[1][2] and third_attr in G[1][2]

