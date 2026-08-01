
def test_extended_barabasi_albert_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.extended_barabasi_albert_graph(10, 2, 0.2, 0.3, create_using=graphtype)

