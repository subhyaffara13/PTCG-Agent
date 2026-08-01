
def test_dt_components_large_values():
    ser = pd.Series(
        [
            pd.Timedelta("365 days 23:59:59.999000"),
            None,
        ],
        dtype=ArrowDtype(pa.duration("ns")),
    )
    result = ser.dt.components
    expected = pd.DataFrame(
        [
            [365, 23, 59, 59, 999, 0, 0],
            [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA],
        ],
        columns=[
            "days",
            "hours",
            "minutes",
            "seconds",
            "milliseconds",
            "microseconds",
            "nanoseconds",
        ],
        dtype="int32[pyarrow]",
    )
    tm.assert_frame_equal(result, expected)

