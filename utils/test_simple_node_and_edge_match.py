
def test_simple_node_and_edge_match(graph_class):
    g1 = graph_class()
    g1.add_weighted_edges_from([(0, 0, 1.2), (0, 1, 1.4), (1, 0, 1.6)])
    g2 = g1.copy()
    nm = iso.numerical_node_match("size", 1)
    if g1.is_multigraph():
        em = iso.numerical_multiedge_match("weight", 1)
    else:
        em = iso.numerical_edge_match("weight", 1)
    assert is_isomorphic(g1, g2, node_match=nm, edge_match=em)

    g2.nodes[0]["size"] = 3
    assert not is_isomorphic(g1, g2, node_match=nm, edge_match=em)

    g2 = g1.copy()
    if g1.is_multigraph():
        g2.edges[0, 1, 0]["weight"] = 2.1
    else:
        g2.edges[0, 1]["weight"] = 2.1
    assert not is_isomorphic(g1, g2, node_match=nm, edge_match=em)

    g2 = g1.copy()
    g2.nodes[0]["size"] = 3
    if g1.is_multigraph():
        g2.edges[0, 1, 0]["weight"] = 2.1
    else:
        g2.edges[0, 1]["weight"] = 2.1
    assert not is_isomorphic(g1, g2, node_match=nm, edge_match=em)

