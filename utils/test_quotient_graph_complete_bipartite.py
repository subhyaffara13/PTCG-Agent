
def test_quotient_graph_complete_bipartite():
    """Tests that the quotient graph of the complete bipartite graph under
    the "same neighbors" node relation is `K_2`.

    """
    G = nx.complete_bipartite_graph(2, 3)
    # Two nodes are equivalent if they are not adjacent but have the same
    # neighbor set.

    def same_neighbors(u, v):
        return u not in G[v] and v not in G[u] and G[u] == G[v]

    expected = nx.complete_graph(2)
    actual = nx.quotient_graph(G, same_neighbors)
    # It won't take too long to run a graph isomorphism algorithm on such
    # small graphs.
    assert nx.is_isomorphic(expected, actual)

