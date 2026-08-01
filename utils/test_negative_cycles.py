
def test_negative_cycles():
    # create a small graph with a negative cycle
    graph = np.ones([5, 5])
    graph.flat[::6] = 0
    graph[1, 2] = -2

    def check(method, directed):
        assert_raises(NegativeCycleError, shortest_path, graph, method,
                      directed)

    for directed in (True, False):
        for method in ['FW', 'J', 'BF']:
            check(method, directed)

        assert_raises(NegativeCycleError, yen, graph, 0, 1, 1,
                      directed=directed)

