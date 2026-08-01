
def test_hermite_domain():
    # Regression test for gh-11091.
    assert np.isnan(_ufuncs.eval_hermite(-1, 1.0))
    assert np.isnan(_ufuncs.eval_hermitenorm(-1, 1.0))

