
def test_construct_shortest_path():
    def check(method, directed):
        SP1, pred = shortest_path(directed_G,
                                  directed=directed,
                                  overwrite=False,
                                  return_predecessors=True)
        SP2 = construct_dist_matrix(directed_G, pred, directed=directed)
        assert_array_almost_equal(SP1, SP2)

    for method in methods:
        for directed in (True, False):
            check(method, directed)

