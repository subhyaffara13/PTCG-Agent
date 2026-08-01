
def test_directed():
    def check(method):
        SP = shortest_path(directed_G, method=method, directed=True,
                           overwrite=False)
        assert_array_almost_equal(SP, directed_SP)

    for method in methods:
        check(method)


def test_directed():
    """
    A directed graph with no bi-directional edges should yield different a graph hash
    to the same graph taken as undirected if there are no hash collisions.
    """
    r = 10
    for i in range(r):
        G_directed = nx.gn_graph(10 + r, seed=100 + i)
        G_undirected = nx.to_undirected(G_directed)

        h_directed = nx.weisfeiler_lehman_graph_hash(G_directed)
        h_undirected = nx.weisfeiler_lehman_graph_hash(G_undirected)

        assert h_directed != h_undirected


def test_directed():
    G = nx.DiGraph([(0, 1), (1, 2), (2, 0)])
    num_walks = nx.number_of_walks(G, 3)
    expected = {0: {0: 1, 1: 0, 2: 0}, 1: {0: 0, 1: 1, 2: 0}, 2: {0: 0, 1: 0, 2: 1}}
    assert num_walks == expected


def test_directed():
    with pytest.raises(nx.NetworkXNotImplemented):
        G = nx.gnp_random_graph(10, 0.2, directed=True, seed=42)
        nx.k_components(G)


def test_directed():
    with pytest.raises(nx.NetworkXNotImplemented):
        G = nx.gnp_random_graph(10, 0.4, directed=True)
        kc = k_components(G)

