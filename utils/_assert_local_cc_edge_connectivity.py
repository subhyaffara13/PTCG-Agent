
def _assert_local_cc_edge_connectivity(G, ccs_local, k, memo):
    """
    tests properties of k-edge-connected components

    the local edge connectivity between each pair of nodes in the original
    graph should be no less than k unless the cc is a single node.
    """
    for cc in ccs_local:
        if len(cc) > 1:
            # Strategy for testing a bit faster: If the subgraph has high edge
            # connectivity then it must have local connectivity
            C = G.subgraph(cc)
            connectivity = nx.edge_connectivity(C)
            if connectivity < k:
                # Otherwise do the brute force (with memoization) check
                _all_pairs_connectivity(G, cc, k, memo)

