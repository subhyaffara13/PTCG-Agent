
def test_local_subgraph_difference_directed():
    dipaths = [(1, 2, 3, 4, 1), (1, 3, 1)]
    G = nx.DiGraph(it.chain(*[pairwise(path) for path in dipaths]))

    assert fset(nx.k_edge_components(G, k=1)) == fset(nx.k_edge_subgraphs(G, k=1))

    # Unlike undirected graphs, when k=2, for directed graphs there is a case
    # where the k-edge-ccs are not the same as the k-edge-subgraphs.
    # (in directed graphs ccs and subgraphs are the same when k=2)
    assert fset(nx.k_edge_components(G, k=2)) != fset(nx.k_edge_subgraphs(G, k=2))

    assert fset(nx.k_edge_components(G, k=3)) == fset(nx.k_edge_subgraphs(G, k=3))

    _check_edge_connectivity(G)

