
def test_triangles():
    paths = [
        (11, 12, 13, 11),  # first 3-clique
        (21, 22, 23, 21),  # second 3-clique
        (11, 21),  # connected by an edge
    ]
    G = nx.Graph(it.chain(*[pairwise(path) for path in paths]))

    # subgraph and ccs are the same in all cases here
    assert fset(nx.k_edge_components(G, k=1)) == fset(nx.k_edge_subgraphs(G, k=1))

    assert fset(nx.k_edge_components(G, k=2)) == fset(nx.k_edge_subgraphs(G, k=2))

    assert fset(nx.k_edge_components(G, k=3)) == fset(nx.k_edge_subgraphs(G, k=3))

    _check_edge_connectivity(G)

