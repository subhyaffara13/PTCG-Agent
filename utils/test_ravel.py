
def test_ravel(index):
    # GH#19956 ravel returning ndarray is deprecated, in 2.0 returns a view on self
    res = index.ravel()
    tm.assert_index_equal(res, index)

