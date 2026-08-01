
def test_rolling_timedelta_window_non_nanoseconds(unit, tz):
    # Test Sum, GH#55106
    df_time = DataFrame(
        {"A": range(5)},
        index=date_range("2013-01-01", freq="1s", periods=5, tz=tz, unit="ns"),
    )
    sum_in_nanosecs = df_time.rolling("1s").sum()
    # microseconds / milliseconds should not break the correct rolling
    df_time.index = df_time.index.as_unit(unit)
    sum_in_microsecs = df_time.rolling("1s").sum()
    sum_in_microsecs.index = sum_in_microsecs.index.as_unit("ns")
    tm.assert_frame_equal(sum_in_nanosecs, sum_in_microsecs)

    # Test max, GH#55026
    ref_dates = date_range("2023-01-01", "2023-01-10", unit="ns", tz=tz)
    ref_series = Series(0, index=ref_dates)
    ref_series.iloc[0] = 1
    ref_max_series = ref_series.rolling(Timedelta(days=4)).max()

    dates = date_range("2023-01-01", "2023-01-10", unit=unit, tz=tz)
    series = Series(0, index=dates)
    series.iloc[0] = 1
    max_series = series.rolling(Timedelta(days=4)).max()

    ref_df = DataFrame(ref_max_series)
    df = DataFrame(max_series)
    df.index = df.index.as_unit("ns")

    tm.assert_frame_equal(ref_df, df)

