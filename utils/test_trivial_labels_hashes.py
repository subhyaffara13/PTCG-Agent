
def test_trivial_labels_hashes():
    """
    Test that 'empty' labelling of nodes or edges shouldn't have a different impact
    on the calculated hash. Note that we cannot assume that trivial weights have no
    impact at all. Without (trivial) weights, a node will start with hashing its
    degree. This step is omitted when there are weights.
    """
    n, r = 100, 10
    p = 1.0 / r
    for i in range(1, r + 1):
        G1 = nx.erdos_renyi_graph(n, p * i, seed=500 + i)
        nx.set_node_attributes(G1, values="", name="weight")
        first = nx.weisfeiler_lehman_graph_hash(G1, node_attr="weight")
        nx.set_edge_attributes(G1, values="", name="e_weight")
        second = nx.weisfeiler_lehman_graph_hash(G1, edge_attr="e_weight")
        assert first == second
        third = nx.weisfeiler_lehman_graph_hash(
            G1, edge_attr="e_weight", node_attr="weight"
        )
        assert second == third

