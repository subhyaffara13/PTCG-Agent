
def test_tarjan_bridge():
    # graph from tarjan paper
    # RE Tarjan - "A note on finding the bridges of a graph"
    # Information Processing Letters, 1974 - Elsevier
    # doi:10.1016/0020-0190(74)90003-9.
    # define 2-connected components and bridges
    ccs = [
        (1, 2, 4, 3, 1, 4),
        (5, 6, 7, 5),
        (8, 9, 10, 8),
        (17, 18, 16, 15, 17),
        (11, 12, 14, 13, 11, 14),
    ]
    bridges = [(4, 8), (3, 5), (3, 17)]
    G = nx.Graph(it.chain(*(pairwise(path) for path in ccs + bridges)))
    _check_edge_connectivity(G)

