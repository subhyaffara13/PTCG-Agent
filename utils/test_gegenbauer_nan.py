
def test_gegenbauer_nan(n, alpha, x):
    # Regression test for gh-11370.
    nan_gegenbauer = np.isnan(_ufuncs.eval_gegenbauer(n, alpha, x))
    nan_arg = np.any(np.isnan([n, alpha, x]))
    assert nan_gegenbauer == nan_arg

