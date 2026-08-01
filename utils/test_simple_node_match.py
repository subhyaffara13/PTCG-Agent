
def test_simple_node_match(graph_class):
    g1 = graph_class([(0, 0), (0, 1), (1, 0)])
    g2 = g1.copy()
    nm = iso.numerical_node_match("size", 1)
    assert is_isomorphic(g1, g2, node_match=nm)

    g2.nodes[0]["size"] = 3
    assert not is_isomorphic(g1, g2, node_match=nm)

