
def test_genlaguerre_nan(n, alpha, x):
    # Regression test for gh-11361.
    nan_laguerre = np.isnan(_ufuncs.eval_genlaguerre(n, alpha, x))
    nan_arg = np.any(np.isnan([n, alpha, x]))
    assert nan_laguerre == nan_arg

