
def test_positive_iters():
    G1 = nx.empty_graph()
    with pytest.raises(
        ValueError,
        match="The WL algorithm requires that `iterations` be positive",
    ):
        nx.weisfeiler_lehman_graph_hash(G1, iterations=-3)
    with pytest.raises(
        ValueError,
        match="The WL algorithm requires that `iterations` be positive",
    ):
        nx.weisfeiler_lehman_subgraph_hashes(G1, iterations=-3)
    with pytest.raises(
        ValueError,
        match="The WL algorithm requires that `iterations` be positive",
    ):
        nx.weisfeiler_lehman_graph_hash(G1, iterations=0)
    with pytest.raises(
        ValueError,
        match="The WL algorithm requires that `iterations` be positive",
    ):
        nx.weisfeiler_lehman_subgraph_hashes(G1, iterations=0)

