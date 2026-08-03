import itertools

def test_all_node_cuts_sap():
    """Non-slow test for `all_node_cuts` using the shortest augmenting path flow."""
    G = nx.cycle_graph(5)
    node_conn = nx.node_connectivity(G)
    all_cuts = nx.all_node_cuts(G, flow_func=flow.shortest_augmenting_path)
    # Only test a limited number of cut sets to reduce test time.
    for cut in itertools.islice(all_cuts, MAX_CUTSETS_TO_TEST):
        assert node_conn == len(cut)
        assert not nx.is_connected(nx.restricted_view(G, cut, []))

