
def test_quotient_graph_complete_multipartite():
    """Tests that the quotient graph of the complete *n*-partite graph
    under the "same neighbors" node relation is the complete graph on *n*
    nodes.

    """
    G = nx.complete_multipartite_graph(2, 3, 4)
    # Two nodes are equivalent if they are not adjacent but have the same
    # neighbor set.

    def same_neighbors(u, v):
        return u not in G[v] and v not in G[u] and G[u] == G[v]

    expected = nx.complete_graph(3)
    actual = nx.quotient_graph(G, same_neighbors)
    # It won't take too long to run a graph isomorphism algorithm on such
    # small graphs.
    assert nx.is_isomorphic(expected, actual)

