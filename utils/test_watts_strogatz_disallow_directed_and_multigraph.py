
def test_watts_strogatz_disallow_directed_and_multigraph(fn, graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        fn(10, 2, 0.2, create_using=graphtype)

