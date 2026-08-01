
def test_trivial_labels_isomorphism_directed():
    """
    Trivial labelling of the graph should not change isomorphism verdicts on digraphs.
    """
    n, r = 100, 10
    p = 1.0 / r
    for i in range(1, r + 1):
        G1 = nx.erdos_renyi_graph(n, p * i, directed=True, seed=500 + i)
        G2 = nx.erdos_renyi_graph(n, p * i, directed=True, seed=42 + i)
        G1_hash = nx.weisfeiler_lehman_graph_hash(G1)
        G2_hash = nx.weisfeiler_lehman_graph_hash(G2)
        equal = G1_hash == G2_hash

        nx.set_node_attributes(G1, values=1, name="weight")
        nx.set_node_attributes(G2, values=1, name="weight")
        G1_hash_node = nx.weisfeiler_lehman_graph_hash(G1, node_attr="weight")
        G2_hash_node = nx.weisfeiler_lehman_graph_hash(G2, node_attr="weight")
        equal_node = G1_hash_node == G2_hash_node

        nx.set_edge_attributes(G1, values="a", name="e_weight")
        nx.set_edge_attributes(G2, values="a", name="e_weight")
        G1_hash_edge = nx.weisfeiler_lehman_graph_hash(G1, edge_attr="e_weight")
        G2_hash_edge = nx.weisfeiler_lehman_graph_hash(G2, edge_attr="e_weight")
        equal_edge = G1_hash_edge == G2_hash_edge

        G1_hash_both = nx.weisfeiler_lehman_graph_hash(
            G1, edge_attr="e_weight", node_attr="weight"
        )
        G2_hash_both = nx.weisfeiler_lehman_graph_hash(
            G2, edge_attr="e_weight", node_attr="weight"
        )
        equal_both = G1_hash_both == G2_hash_both

        assert equal == equal_node
        assert equal_node == equal_edge
        assert equal_edge == equal_both

    # Specific case that was found to be a bug in issue #7806
    # Without weights worked
    Ga = nx.DiGraph()
    Ga.add_nodes_from([1, 2, 3, 4])
    Gb = copy.deepcopy(Ga)
    Ga.add_edges_from([(1, 2), (3, 2)])
    Gb.add_edges_from([(1, 2), (3, 4)])
    Ga_hash = nx.weisfeiler_lehman_graph_hash(Ga)
    Gb_hash = nx.weisfeiler_lehman_graph_hash(Gb)
    assert Ga_hash != Gb_hash

    # Now with trivial weights
    nx.set_node_attributes(Ga, values=1, name="weight")
    nx.set_node_attributes(Gb, values=1, name="weight")
    Ga_hash = nx.weisfeiler_lehman_graph_hash(Ga, node_attr="weight")
    Gb_hash = nx.weisfeiler_lehman_graph_hash(Gb, node_attr="weight")
    assert Ga_hash != Gb_hash

