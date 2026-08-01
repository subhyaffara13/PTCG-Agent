
def test_bridge_cc():
    # define 2-connected components and bridges
    cc2 = [(1, 2, 4, 3, 1, 4), (8, 9, 10, 8), (11, 12, 13, 11)]
    bridges = [(4, 8), (3, 5), (20, 21), (22, 23, 24)]
    G = nx.Graph(it.chain(*(pairwise(path) for path in cc2 + bridges)))
    bridge_ccs = fset(bridge_components(G))
    target_ccs = fset(
        [{1, 2, 3, 4}, {5}, {8, 9, 10}, {11, 12, 13}, {20}, {21}, {22}, {23}, {24}]
    )
    assert bridge_ccs == target_ccs
    _check_edge_connectivity(G)

