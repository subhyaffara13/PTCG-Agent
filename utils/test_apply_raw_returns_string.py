
def test_apply_raw_returns_string(engine):
    # https://github.com/pandas-dev/pandas/issues/35940
    if engine == "numba":
        pytest.skip("No object dtype support in numba")
    df = DataFrame({"A": ["aa", "bbb"]})
    result = df.apply(lambda x: x[0], engine=engine, axis=1, raw=True)
    expected = Series(["aa", "bbb"])
    tm.assert_series_equal(result, expected)

