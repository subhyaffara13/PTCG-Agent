
def test_to_datetime_mixed_not_necessarily_iso8601_coerce():
    # https://github.com/pandas-dev/pandas/issues/50411
    result = to_datetime(
        ["2020-01-01", "01-01-2000"], format="ISO8601", errors="coerce"
    )
    tm.assert_index_equal(result, DatetimeIndex(["2020-01-01 00:00:00", NaT]))

