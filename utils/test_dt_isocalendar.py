
def test_dt_isocalendar():
    ser = pd.Series(
        [datetime(year=2023, month=1, day=2, hour=3), None],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    result = ser.dt.isocalendar()
    expected = pd.DataFrame(
        [[2023, 1, 1], [0, 0, 0]],
        columns=["year", "week", "day"],
        dtype="int64[pyarrow]",
    )
    tm.assert_frame_equal(result, expected)

