
def test_get_nan_multiple(float_numpy_dtype):
    # GH 8569
    # ensure that fixing "test_get_nan" above hasn't broken get
    # with multiple elements
    s = Index(range(10), dtype=float_numpy_dtype).to_series()

    idx = [2, 30]
    assert s.get(idx) is None

    idx = [2, np.nan]
    assert s.get(idx) is None

    # GH 17295 - all missing keys
    idx = [20, 30]
    assert s.get(idx) is None

    idx = [np.nan, np.nan]
    assert s.get(idx) is None

