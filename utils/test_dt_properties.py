
def test_dt_properties(prop, expected):
    ser = pd.Series(
        [
            pd.Timestamp(
                year=2023,
                month=1,
                day=2,
                hour=3,
                minute=4,
                second=7,
                microsecond=2000,
                nanosecond=6,
            ),
            None,
        ],
        dtype=ArrowDtype(pa.timestamp("ns")),
    )
    result = getattr(ser.dt, prop)
    exp_type = None
    if isinstance(expected, date):
        exp_type = pa.date32()
    elif isinstance(expected, time):
        exp_type = pa.time64("ns")
    expected = pd.Series(ArrowExtensionArray(pa.array([expected, None], type=exp_type)))
    tm.assert_series_equal(result, expected)

