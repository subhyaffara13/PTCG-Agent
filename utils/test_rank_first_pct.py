
def test_rank_first_pct(dtype, ser, exp):
    if ser[0] < 0 and dtype.startswith("str"):
        exp = exp[::-1]
    s = Series(ser).astype(dtype)
    result = s.rank(method="first", pct=True)
    expected = Series(exp).astype(expected_dtype(dtype, "first", pct=True))
    tm.assert_series_equal(result, expected)

