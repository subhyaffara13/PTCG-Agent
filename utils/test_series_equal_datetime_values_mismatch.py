
def test_series_equal_datetime_values_mismatch(rtol):
    msg = """Series are different

Series values are different \\(100.0 %\\)
\\[index\\]: \\[0, 1, 2\\]
\\[left\\]:  \\[1514764800000000000, 1514851200000000000, 1514937600000000000\\]
\\[right\\]: \\[1549065600000000000, 1549152000000000000, 1549238400000000000\\]"""

    s1 = Series(pd.date_range("2018-01-01", periods=3, freq="D", unit="ns"))
    s2 = Series(pd.date_range("2019-02-02", periods=3, freq="D", unit="ns"))

    with pytest.raises(AssertionError, match=msg):
        tm.assert_series_equal(s1, s2, rtol=rtol)

