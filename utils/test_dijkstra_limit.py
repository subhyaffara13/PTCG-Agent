
def test_dijkstra_limit():
    limits = [0, 2, np.inf]
    results = [undirected_SP_limit_0,
               undirected_SP_limit_2,
               undirected_SP]

    def check(limit, result):
        SP = dijkstra(undirected_G, directed=False, limit=limit)
        assert_array_almost_equal(SP, result)

    for limit, result in zip(limits, results):
        check(limit, result)

