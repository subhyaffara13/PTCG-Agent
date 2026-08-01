
def test_steiner_tree_weight_attribute(method):
    G = nx.star_graph(4)
    # Add an edge attribute that is named something other than "weight"
    nx.set_edge_attributes(G, {e: 10 for e in G.edges}, name="distance")
    H = nx.approximation.steiner_tree(G, [1, 3], method=method, weight="distance")
    assert nx.utils.edges_equal(H.edges, [(0, 1), (0, 3)])

