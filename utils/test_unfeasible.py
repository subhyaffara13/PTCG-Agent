
def test_unfeasible():
    G = tarjan_bridge_graph()
    pytest.raises(nx.NetworkXUnfeasible, list, k_edge_augmentation(G, k=1, avail=[]))

    pytest.raises(nx.NetworkXUnfeasible, list, k_edge_augmentation(G, k=2, avail=[]))

    pytest.raises(
        nx.NetworkXUnfeasible, list, k_edge_augmentation(G, k=2, avail=[(7, 9)])
    )

    # partial solutions should not error if real solutions are infeasible
    aug_edges = list(k_edge_augmentation(G, k=2, avail=[(7, 9)], partial=True))
    assert aug_edges == [(7, 9)]

    _check_augmentations(G, avail=[], max_k=MAX_EFFICIENT_K + 2)

    _check_augmentations(G, avail=[(7, 9)], max_k=MAX_EFFICIENT_K + 2)

