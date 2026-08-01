
def test_greedy_multigraph_disallowed():
    with pytest.raises(nx.NetworkXNotImplemented):
        nx.community.greedy_node_swap_bipartition(nx.MultiGraph())

