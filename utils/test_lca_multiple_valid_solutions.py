
def test_lca_multiple_valid_solutions():
    G = nx.DiGraph()
    G.add_nodes_from(range(4))
    G.add_edges_from([(2, 0), (3, 0), (2, 1), (3, 1)])
    assert nx.lowest_common_ancestor(G, 0, 1) in {2, 3}

