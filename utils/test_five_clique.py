
def test_five_clique():
    # Make a graph that can be disconnected less than 4 edges, but no node has
    # degree less than 4.
    G = nx.disjoint_union(nx.complete_graph(5), nx.complete_graph(5))
    paths = [
        # add aux-connections
        (1, 100, 6),
        (2, 100, 7),
        (3, 200, 8),
        (4, 200, 100),
    ]
    G.add_edges_from(it.chain(*[pairwise(path) for path in paths]))
    assert min(dict(nx.degree(G)).values()) == 4

    # For k=3 they are the same
    assert fset(nx.k_edge_components(G, k=3)) == fset(nx.k_edge_subgraphs(G, k=3))

    # For k=4 they are the different
    # the aux nodes are in the same CC as clique 1 but no the same subgraph
    assert fset(nx.k_edge_components(G, k=4)) != fset(nx.k_edge_subgraphs(G, k=4))

    # For k=5 they are not the same
    assert fset(nx.k_edge_components(G, k=5)) != fset(nx.k_edge_subgraphs(G, k=5))

    # For k=6 they are the same
    assert fset(nx.k_edge_components(G, k=6)) == fset(nx.k_edge_subgraphs(G, k=6))
    _check_edge_connectivity(G)

