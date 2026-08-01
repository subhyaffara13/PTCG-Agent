
def test_initial_node_labels_subgraph_hash():
    """
    Including the hashed initial label prepends an extra hash to the lists
    """
    G = nx.path_graph(5)
    nx.set_node_attributes(G, {i: int(0 < i < 4) for i in G}, "label")
    # initial node labels:
    # 0--1--1--1--0

    without_initial_label = nx.weisfeiler_lehman_subgraph_hashes(G, node_attr="label")
    assert all(len(v) == 3 for v in without_initial_label.values())
    # 3 different 1 hop nhds
    assert len({v[0] for v in without_initial_label.values()}) == 3

    with_initial_label = nx.weisfeiler_lehman_subgraph_hashes(
        G, node_attr="label", include_initial_labels=True
    )
    assert all(len(v) == 4 for v in with_initial_label.values())
    # 2 different initial labels
    assert len({v[0] for v in with_initial_label.values()}) == 2

    # check hashes match otherwise
    for u in G:
        for a, b in zip(
            with_initial_label[u][1:], without_initial_label[u], strict=True
        ):
            assert a == b

