
def test_unweighted_path():
    def check(method, directed):
        SP1 = shortest_path(directed_G,
                            directed=directed,
                            overwrite=False,
                            unweighted=True)
        SP2 = shortest_path(unweighted_G,
                            directed=directed,
                            overwrite=False,
                            unweighted=False)
        assert_array_almost_equal(SP1, SP2)

    for method in methods:
        for directed in (True, False):
            check(method, directed)

