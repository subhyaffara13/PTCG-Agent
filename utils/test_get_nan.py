
def test_get_nan(float_numpy_dtype):
    # GH 8569
    s = Index(range(10), dtype=float_numpy_dtype).to_series()
    assert s.get(np.nan) is None
    assert s.get(np.nan, default="Missing") == "Missing"

