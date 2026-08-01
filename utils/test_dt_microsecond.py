
def test_dt_microsecond(microsecond):
    # GH 59183
    ser = pd.Series(
        [
            pd.Timestamp(
                year=2024,
                month=7,
                day=7,
                second=5,
                microsecond=microsecond,
                nanosecond=6,
            ),
            None,
        ],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    result = ser.dt.microsecond
    expected = pd.Series([microsecond, None], dtype="int64[pyarrow]")
    tm.assert_series_equal(result, expected)

