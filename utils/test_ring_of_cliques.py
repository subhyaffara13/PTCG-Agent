
def test_ring_of_cliques():
    for i in range(2, 20, 3):
        for j in range(2, 20, 3):
            G = nx.ring_of_cliques(i, j)
            assert G.number_of_nodes() == i * j
            if i != 2 or j != 1:
                expected_num_edges = i * (((j * (j - 1)) // 2) + 1)
            else:
                # the edge that already exists cannot be duplicated
                expected_num_edges = i * (((j * (j - 1)) // 2) + 1) - 1
            assert G.number_of_edges() == expected_num_edges
    with pytest.raises(
        nx.NetworkXError, match="A ring of cliques must have at least two cliques"
    ):
        nx.ring_of_cliques(1, 5)
    with pytest.raises(
        nx.NetworkXError, match="The cliques must have at least two nodes"
    ):
        nx.ring_of_cliques(3, 0)

