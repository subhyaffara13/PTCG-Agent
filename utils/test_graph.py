
def test_graph():
    G = nx.path_graph(4)
    H = cytoscape_graph(cytoscape_data(G))
    assert nx.is_isomorphic(G, H)


def test_graph():
    G = nx.DiGraph()
    G.add_nodes_from([1, 2, 3], color="red")
    G.add_edge(1, 2, foo=7)
    G.add_edge(1, 3, foo=10)
    G.add_edge(3, 4, foo=10)
    H = tree_graph(tree_data(G, 1))
    assert nx.is_isomorphic(G, H)

