
def _check_edge_connectivity(G):
    """
    Helper - generates all k-edge-components using the aux graph.  Checks the
    both local and subgraph edge connectivity of each cc. Also checks that
    alternate methods of computing the k-edge-ccs generate the same result.
    """
    # Construct the auxiliary graph that can be used to make each k-cc or k-sub
    aux_graph = EdgeComponentAuxGraph.construct(G)

    # memoize the local connectivity in this graph
    memo = {}

    for k in it.count(1):
        # Test "local" k-edge-components and k-edge-subgraphs
        ccs_local = fset(aux_graph.k_edge_components(k))
        ccs_subgraph = fset(aux_graph.k_edge_subgraphs(k))

        # Check connectivity properties that should be guaranteed by the
        # algorithms.
        _assert_local_cc_edge_connectivity(G, ccs_local, k, memo)
        _assert_subgraph_edge_connectivity(G, ccs_subgraph, k)

        if k == 1 or k == 2 and not G.is_directed():
            assert ccs_local == ccs_subgraph, (
                "Subgraphs and components should be the same when k == 1 or (k == 2 and not G.directed())"
            )

        if G.is_directed():
            # Test special case methods are the same as the aux graph
            if k == 1:
                alt_sccs = fset(nx.strongly_connected_components(G))
                assert alt_sccs == ccs_local, "k=1 failed alt"
                assert alt_sccs == ccs_subgraph, "k=1 failed alt"
        else:
            # Test special case methods are the same as the aux graph
            if k == 1:
                alt_ccs = fset(nx.connected_components(G))
                assert alt_ccs == ccs_local, "k=1 failed alt"
                assert alt_ccs == ccs_subgraph, "k=1 failed alt"
            elif k == 2:
                alt_bridge_ccs = fset(bridge_components(G))
                assert alt_bridge_ccs == ccs_local, "k=2 failed alt"
                assert alt_bridge_ccs == ccs_subgraph, "k=2 failed alt"
            # if new methods for k == 3 or k == 4 are implemented add them here

        # Check the general subgraph method works by itself
        alt_subgraph_ccs = fset(
            [set(C.nodes()) for C in general_k_edge_subgraphs(G, k=k)]
        )
        assert alt_subgraph_ccs == ccs_subgraph, "alt subgraph method failed"

        # Stop once k is larger than all special case methods
        # and we cannot break down ccs any further.
        if k > 2 and all(len(cc) == 1 for cc in ccs_local):
            break

