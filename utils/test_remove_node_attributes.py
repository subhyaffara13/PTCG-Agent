
def test_remove_node_attributes(graph_type):
    # Test removing single attribute
    G = nx.path_graph(3, create_using=graph_type)
    vals = 100
    attr = "hello"
    nx.set_node_attributes(G, vals, attr)
    nx.remove_node_attributes(G, attr)
    assert attr not in G.nodes[0]
    assert attr not in G.nodes[1]
    assert attr not in G.nodes[2]

    # Test removing single attribute when multiple present
    G = nx.path_graph(3, create_using=graph_type)
    other_vals = 200
    other_attr = "other"
    nx.set_node_attributes(G, vals, attr)
    nx.set_node_attributes(G, other_vals, other_attr)
    nx.remove_node_attributes(G, attr)
    assert attr not in G.nodes[0]
    assert G.nodes[0][other_attr] == other_vals
    assert attr not in G.nodes[1]
    assert G.nodes[1][other_attr] == other_vals
    assert attr not in G.nodes[2]
    assert G.nodes[2][other_attr] == other_vals

    # Test removing multiple attributes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_node_attributes(G, vals, attr)
    nx.set_node_attributes(G, other_vals, other_attr)
    nx.remove_node_attributes(G, attr, other_attr)
    assert attr not in G.nodes[0] and other_attr not in G.nodes[0]
    assert attr not in G.nodes[1] and other_attr not in G.nodes[1]
    assert attr not in G.nodes[2] and other_attr not in G.nodes[2]

    # Test removing multiple (but not all) attributes
    G = nx.path_graph(3, create_using=graph_type)
    third_vals = 300
    third_attr = "three"
    nx.set_node_attributes(
        G,
        {
            n: {attr: vals, other_attr: other_vals, third_attr: third_vals}
            for n in G.nodes()
        },
    )
    nx.remove_node_attributes(G, other_attr, third_attr)
    assert other_attr not in G.nodes[0] and third_attr not in G.nodes[0]
    assert other_attr not in G.nodes[1] and third_attr not in G.nodes[1]
    assert other_attr not in G.nodes[2] and third_attr not in G.nodes[2]
    assert G.nodes[0][attr] == vals
    assert G.nodes[1][attr] == vals
    assert G.nodes[2][attr] == vals

    # Test incomplete node attributes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_node_attributes(
        G,
        {
            1: {attr: vals, other_attr: other_vals},
            2: {attr: vals, other_attr: other_vals},
        },
    )
    nx.remove_node_attributes(G, attr)
    assert attr not in G.nodes[0]
    assert attr not in G.nodes[1]
    assert attr not in G.nodes[2]
    assert G.nodes[1][other_attr] == other_vals
    assert G.nodes[2][other_attr] == other_vals

    # Test removing on a subset of nodes
    G = nx.path_graph(3, create_using=graph_type)
    nx.set_node_attributes(
        G,
        {
            n: {attr: vals, other_attr: other_vals, third_attr: third_vals}
            for n in G.nodes()
        },
    )
    nx.remove_node_attributes(G, attr, other_attr, nbunch=[0, 1])
    assert attr not in G.nodes[0] and other_attr not in G.nodes[0]
    assert attr not in G.nodes[1] and other_attr not in G.nodes[1]
    assert attr in G.nodes[2] and other_attr in G.nodes[2]
    assert third_attr in G.nodes[0] and G.nodes[0][third_attr] == third_vals
    assert third_attr in G.nodes[1] and G.nodes[1][third_attr] == third_vals

