
def test_undirected_sparse_zero():
    def check(method, directed_in):
        if directed_in:
            SP1 = shortest_path(directed_sparse_zero_G, method=method, directed=False,
                                overwrite=False)
            assert_array_almost_equal(SP1, undirected_sparse_zero_SP)
        else:
            SP2 = shortest_path(undirected_sparse_zero_G, method=method, directed=True,
                                overwrite=False)
            assert_array_almost_equal(SP2, undirected_sparse_zero_SP)

    for method in methods:
        for directed_in in (True, False):
            check(method, directed_in)

