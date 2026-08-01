
def test_directed_sparse_zero():
    # test directed sparse graph with zero-weight edge and two connected components
    def check(method):
        SP = shortest_path(directed_sparse_zero_G, method=method, directed=True,
                           overwrite=False)
        assert_array_almost_equal(SP, directed_sparse_zero_SP)

    for method in methods:
        check(method)

