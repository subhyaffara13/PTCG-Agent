
def test_rolling_min_max_numeric_types(any_real_numpy_dtype):
    # GH12373

    # Just testing that these don't throw exceptions and that
    # the return type is float64. Other tests will cover quantitative
    # correctness
    result = (
        DataFrame(np.arange(20, dtype=any_real_numpy_dtype)).rolling(window=5).max()
    )
    assert result.dtypes[0] == np.dtype("f8")
    result = (
        DataFrame(np.arange(20, dtype=any_real_numpy_dtype)).rolling(window=5).min()
    )
    assert result.dtypes[0] == np.dtype("f8")

