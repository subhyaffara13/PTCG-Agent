
def test_resample_closed_right():
    # GH#45414
    idx = pd.Index([pd.Timedelta(seconds=120 + i * 30) for i in range(10)])
    ser = Series(range(10), index=idx)
    result = ser.resample("min", closed="right", label="right").sum()
    expected = Series(
        [0, 3, 7, 11, 15, 9],
        index=pd.TimedeltaIndex(
            [pd.Timedelta(seconds=120 + i * 60) for i in range(6)], freq="min"
        ),
    )
    tm.assert_series_equal(result, expected)

