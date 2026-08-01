
def test_masked_input():
    np.ma.masked_equal(directed_G, 0)

    def check(method):
        SP = shortest_path(directed_G, method=method, directed=True,
                           overwrite=False)
        assert_array_almost_equal(SP, directed_SP)

    for method in methods:
        check(method)

