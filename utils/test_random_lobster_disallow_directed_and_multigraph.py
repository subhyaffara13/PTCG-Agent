
def test_random_lobster_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.random_lobster_graph(10, 0.1, 0.1, create_using=graphtype)

