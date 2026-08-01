
def test_four_clique():
    paths = [
        (11, 12, 13, 14, 11, 13, 14, 12),  # first 4-clique
        (21, 22, 23, 24, 21, 23, 24, 22),  # second 4-clique
        # paths connecting the 4 cliques such that they are
        # 3-connected in G, but not in the subgraph.
        # Case where the nodes bridging them do not have degree less than 3.
        (100, 13),
        (12, 100, 22),
        (13, 200, 23),
        (14, 300, 24),
    ]
    G = nx.Graph(it.chain(*[pairwise(path) for path in paths]))

    # The subgraphs and ccs are different for k=3
    local_ccs = fset(nx.k_edge_components(G, k=3))
    subgraphs = fset(nx.k_edge_subgraphs(G, k=3))
    assert local_ccs != subgraphs

    # The cliques ares in the same cc
    clique1 = frozenset(paths[0])
    clique2 = frozenset(paths[1])
    assert clique1.union(clique2).union({100}) in local_ccs

    # but different subgraphs
    assert clique1 in subgraphs
    assert clique2 in subgraphs

    assert G.degree(100) == 3

    _check_edge_connectivity(G)

