
def test_where_ndframe_align():
    msg = "Array conditional must be same shape as self"
    s = Series([1, 2, 3])

    cond = [True]
    with pytest.raises(ValueError, match=msg):
        s.where(cond)

    expected = Series([1, np.nan, np.nan])

    out = s.where(Series(cond))
    tm.assert_series_equal(out, expected)

    cond = np.array([False, True, False, True])
    with pytest.raises(ValueError, match=msg):
        s.where(cond)

    expected = Series([np.nan, 2, np.nan])

    out = s.where(Series(cond))
    tm.assert_series_equal(out, expected)

