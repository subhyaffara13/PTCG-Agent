
def test_attr_wrapper(ts):
    grouped = ts.groupby(lambda x: x.weekday())

    result = grouped.std()
    expected = grouped.agg(lambda x: np.std(x, ddof=1))
    tm.assert_series_equal(result, expected)

    # this is pretty cool
    result = grouped.describe()
    expected = {name: gp.describe() for name, gp in grouped}
    expected = DataFrame(expected).T
    tm.assert_frame_equal(result, expected)

    # get attribute
    result = grouped.dtype
    expected = grouped.agg(lambda x: x.dtype)
    tm.assert_series_equal(result, expected)

    # make sure raises error
    msg = "'SeriesGroupBy' object has no attribute 'foo'"
    with pytest.raises(AttributeError, match=msg):
        grouped.foo

