
def test_equivalence_non_subset():
    """Assert that subset betweenness centrality with all nodes in the
    subset is equivalent to full betweenness centrality.
    """
    G = nx.path_graph(10, create_using=nx.DiGraph)

    assert nx.betweenness_centrality(G) == nx.betweenness_centrality_subset(
        G, sources=G.nodes(), targets=G.nodes(), normalized=True
    )
    assert nx.edge_betweenness_centrality(G) == nx.edge_betweenness_centrality_subset(
        G, sources=G.nodes(), targets=G.nodes(), normalized=True
    )

