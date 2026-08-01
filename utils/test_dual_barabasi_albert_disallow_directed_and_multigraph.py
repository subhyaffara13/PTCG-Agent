
def test_dual_barabasi_albert_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.dual_barabasi_albert_graph(10, 2, 1, 0.4, create_using=graphtype)

