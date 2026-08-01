
def test_random_kernel_disallow_directed_and_multigraph(graphtype):
    with pytest.raises(nx.NetworkXError, match="must not be"):
        nx.random_kernel_graph(
            10, lambda y, a, b: a + b, lambda u, w, r: r + w, create_using=graphtype
        )

