
def test_hermite_nan(n, x):
    # Regression test for gh-11369.
    assert np.isnan(_ufuncs.eval_hermite(n, x)) == np.any(np.isnan([n, x]))
    assert np.isnan(_ufuncs.eval_hermitenorm(n, x)) == np.any(np.isnan([n, x]))

