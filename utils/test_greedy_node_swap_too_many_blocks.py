
def test_greedy_node_swap_too_many_blocks():
    G = nx.barbell_graph(3, 0)
    split = ({0, 1}, {2}, {3, 4, 5})
    with pytest.raises(nx.NetworkXError):
        nx.community.greedy_node_swap_bipartition(G, init_split=split)

