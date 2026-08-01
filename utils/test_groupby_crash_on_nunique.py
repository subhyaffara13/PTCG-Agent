
def test_groupby_crash_on_nunique():
    # Fix following 30253
    dti = date_range("2016-01-01", periods=2, name="foo")
    df = DataFrame({("A", "B"): [1, 2], ("A", "C"): [1, 3], ("D", "B"): [0, 0]})
    df.columns.names = ("bar", "baz")
    df.index = dti

    df = df.T
    gb = df.groupby(level=0)
    result = gb.nunique()

    expected = DataFrame({"A": [1, 2], "D": [1, 1]}, index=dti)
    expected.columns.name = "bar"
    expected = expected.T

    tm.assert_frame_equal(result, expected)

    # same thing, but empty columns
    gb2 = df[[]].groupby(level=0)
    exp = expected[[]]

    res = gb2.nunique()
    tm.assert_frame_equal(res, exp)

