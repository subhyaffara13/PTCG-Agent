
def test_barabasi_albert_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.barabasi_albert_graph(10, 3, create_using=graphtype)

