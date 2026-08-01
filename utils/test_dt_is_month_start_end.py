
def test_dt_is_month_start_end():
    ser = pd.Series(
        [
            datetime(year=2023, month=12, day=2, hour=3),
            datetime(year=2023, month=1, day=1, hour=3),
            datetime(year=2023, month=3, day=31, hour=3),
            None,
        ],
        dtype=ArrowDtype(pa.timestamp("us")),
    )
    result = ser.dt.is_month_start
    expected = pd.Series([False, True, False, None], dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

    result = ser.dt.is_month_end
    expected = pd.Series([False, False, True, None], dtype=ArrowDtype(pa.bool_()))
    tm.assert_series_equal(result, expected)

