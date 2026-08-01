
def test_dt_timedelta_total_seconds():
    # GH 52284
    ser = pd.Series(
        [
            pd.Timedelta(
                days=1,
                seconds=2,
                microseconds=3,
                nanoseconds=4,
            ),
            None,
        ],
        dtype=ArrowDtype(pa.duration("ns")),
    )
    result = ser.dt.total_seconds()
    expected = pd.Series(
        ArrowExtensionArray(pa.array([86402.000003, None], type=pa.float64()))
    )
    tm.assert_series_equal(result, expected)

