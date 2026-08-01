
def _check_multigammaln_array_result(a, d):
    # Test that the shape of the array returned by multigammaln
    # matches the input shape, and that all the values match
    # the value computed when multigammaln is called with a scalar.
    result = multigammaln(a, d)
    assert_array_equal(a.shape, result.shape)
    a1 = a.ravel()
    result1 = result.ravel()
    for i in range(a.size):
        assert_array_almost_equal_nulp(result1[i], multigammaln(a1[i], d))

