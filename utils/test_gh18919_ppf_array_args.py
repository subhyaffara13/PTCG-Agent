
def test_gh18919_ppf_array_args():
    # gh-18919 reported incorrect results for ppf and isf of discrete distributions when
    # arguments were arrays and first argument (`q`) had elements at the boundaries of
    # the support.
    q = [[0.5, 1.0, 0.5],
         [1.0, 0.5, 1.0],
         [0.5, 1.0, 0.5]]

    n = [[45, 46, 47],
         [48, 49, 50],
         [51, 52, 53]]

    p = 0.5

    ref = _ufuncs._binom_ppf(q, n, p)
    res = stats.binom.ppf(q, n, p)
    np.testing.assert_allclose(res, ref)

