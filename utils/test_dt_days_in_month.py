
def test_dt_days_in_month(method):
    ser = pd.Series(
        [
            datetime(year=2023, month=3, day=30, hour=3),
            datetime(year=2023, month=4, day=1, hour=3),
            datetime(year=2023, month=2, day=3, hour=3),
            None,
        ],
        dtype=ArrowDtype(pa.timestamp("us")),
    )
    result = getattr(ser.dt, method)
    expected = pd.Series([31, 30, 28, None], dtype=ArrowDtype(pa.int64()))
    tm.assert_series_equal(result, expected)

