
def test_good_newline_in_iterator(data):
    # The quoted newlines will be untransformed here, but are just whitespace.
    res = np.loadtxt(data, delimiter=",", quotechar="'")
    assert_array_equal(res, [[1., 2.], [2., 3.]])

