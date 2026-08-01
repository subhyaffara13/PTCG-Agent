
def test_random_powerlaw_tree_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.random_powerlaw_tree(10, create_using=graphtype)

