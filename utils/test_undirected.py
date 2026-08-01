
def test_undirected():
    def check(method, directed_in):
        if directed_in:
            SP1 = shortest_path(directed_G, method=method, directed=False,
                                overwrite=False)
            assert_array_almost_equal(SP1, undirected_SP)
        else:
            SP2 = shortest_path(undirected_G, method=method, directed=True,
                                overwrite=False)
            assert_array_almost_equal(SP2, undirected_SP)

    for method in methods:
        for directed_in in (True, False):
            check(method, directed_in)


def test_undirected():
    G = nx.cycle_graph(3)
    num_walks = nx.number_of_walks(G, 3)
    expected = {0: {0: 2, 1: 3, 2: 3}, 1: {0: 3, 1: 2, 2: 3}, 2: {0: 3, 1: 3, 2: 2}}
    assert num_walks == expected

