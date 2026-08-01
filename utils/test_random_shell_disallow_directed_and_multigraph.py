
def test_random_shell_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.random_shell_graph([(10, 20, 2), (10, 20, 5)], create_using=graphtype)

