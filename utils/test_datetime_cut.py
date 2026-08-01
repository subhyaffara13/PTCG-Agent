
def test_datetime_cut(unit, box):
    # see gh-14714
    #
    # Testing time data when it comes in various collection types.
    data = to_datetime(["2013-01-01", "2013-01-02", "2013-01-03"]).astype(f"M8[{unit}]")
    data = box(data)
    result, _ = cut(data, 3, retbins=True)

    if unit == "s":
        # See https://github.com/pandas-dev/pandas/pull/56101#discussion_r1405325425
        # for why we round to 8 seconds instead of 7
        left = DatetimeIndex(
            ["2012-12-31 23:57:08", "2013-01-01 16:00:00", "2013-01-02 08:00:00"],
            dtype=f"M8[{unit}]",
        )
    else:
        left = DatetimeIndex(
            [
                "2012-12-31 23:57:07.200000",
                "2013-01-01 16:00:00",
                "2013-01-02 08:00:00",
            ],
            dtype=f"M8[{unit}]",
        )
    right = DatetimeIndex(
        ["2013-01-01 16:00:00", "2013-01-02 08:00:00", "2013-01-03 00:00:00"],
        dtype=f"M8[{unit}]",
    )

    exp_intervals = IntervalIndex.from_arrays(left, right)
    expected = Series(exp_intervals).astype(CategoricalDtype(ordered=True))
    tm.assert_series_equal(Series(result), expected)

