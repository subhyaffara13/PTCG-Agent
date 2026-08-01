
def test_gnp_fns_disallow_multigraph(fn, directed):
    with pytest.raises(nx.NetworkXError, match="must not be a multi-graph"):
        fn(20, 0.2, create_using=nx.MultiGraph)

