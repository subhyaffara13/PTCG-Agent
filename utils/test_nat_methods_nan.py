
def test_nat_methods_nan(method):
    # see gh-9513, gh-17329
    assert np.isnan(getattr(NaT, method)())

