
def test_junction_tree_directed_unconnected_nodes():
    B = nx.DiGraph()
    B.add_nodes_from([("A", "B", "C", "D")])
    G = junction_tree(B)

    J = nx.Graph()
    J.add_nodes_from([("A", "B", "C", "D")])

    assert nx.is_isomorphic(G, J)

