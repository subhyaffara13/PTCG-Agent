
def test_datetime_cut_roundtrip(tz, unit):
    # see gh-19891
    ser = Series(date_range("20180101", periods=3, tz=tz, unit=unit))
    result, result_bins = cut(ser, 2, retbins=True)

    expected = cut(ser, result_bins)
    tm.assert_series_equal(result, expected)

    if unit == "s":
        # TODO: constructing DatetimeIndex with dtype="M8[s]" without truncating
        #  the first entry here raises in array_to_datetime. Should truncate
        #  instead of raising?
        # See https://github.com/pandas-dev/pandas/pull/56101#discussion_r1405325425
        # for why we round to 8 seconds instead of 7
        expected_bins = DatetimeIndex(
            ["2017-12-31 23:57:08", "2018-01-02 00:00:00", "2018-01-03 00:00:00"],
            dtype=f"M8[{unit}]",
        )
    else:
        expected_bins = DatetimeIndex(
            [
                "2017-12-31 23:57:07.200000",
                "2018-01-02 00:00:00",
                "2018-01-03 00:00:00",
            ],
            dtype=f"M8[{unit}]",
        )
    expected_bins = expected_bins.tz_localize(tz)
    tm.assert_index_equal(result_bins, expected_bins)

