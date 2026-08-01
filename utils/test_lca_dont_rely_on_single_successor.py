
def test_lca_dont_rely_on_single_successor():
    # Nodes 0 and 1 have nodes 2 and 3 as immediate ancestors,
    # and node 2 also has node 3 as an immediate ancestor.
    G = nx.DiGraph()
    G.add_nodes_from(range(4))
    G.add_edges_from([(2, 0), (2, 1), (3, 1), (3, 0), (3, 2)])
    assert nx.lowest_common_ancestor(G, 0, 1) == 2

