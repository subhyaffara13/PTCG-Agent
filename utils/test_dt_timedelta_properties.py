
def test_dt_timedelta_properties(prop, expected):
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
    result = getattr(ser.dt, prop)
    expected = pd.Series(
        ArrowExtensionArray(pa.array([expected, None], type=pa.int32()))
    )
    tm.assert_series_equal(result, expected)

