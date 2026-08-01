
def test_explode_scalars_can_ignore_index():
    # https://github.com/pandas-dev/pandas/issues/40487
    s = pd.Series([1, 2, 3], index=["a", "b", "c"])
    result = s.explode(ignore_index=True)
    expected = pd.Series([1, 2, 3])
    tm.assert_series_equal(result, expected)

