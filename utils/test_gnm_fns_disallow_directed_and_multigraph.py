
def test_gnm_fns_disallow_directed_and_multigraph(fn, graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        fn(10, 20, create_using=graphtype)

