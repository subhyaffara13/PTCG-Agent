
def test_downcast_float64_to_float32():
    # GH-43693: Check float64 preservation when >= 16,777,217
    series = Series([16777217.0, np.finfo(np.float64).max, np.nan], dtype=np.float64)
    result = to_numeric(series, downcast="float")

    assert series.dtype == result.dtype

