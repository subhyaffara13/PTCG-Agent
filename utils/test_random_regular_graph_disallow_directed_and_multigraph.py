
def test_random_regular_graph_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.random_regular_graph(2, 10, create_using=graphtype)

