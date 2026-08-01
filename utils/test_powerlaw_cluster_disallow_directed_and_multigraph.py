
def test_powerlaw_cluster_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.powerlaw_cluster_graph(10, 5, 0.2, create_using=graphtype)

