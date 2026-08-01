
def test_timeseries_groupby_agg():
    # GH#43290

    def func(ser):
        if ser.isna().all():
            return None
        return np.sum(ser)

    df = DataFrame([1.0], index=[pd.Timestamp("2018-01-16 00:00:00+00:00")])
    res = df.groupby(lambda x: 1).agg(func)

    expected = DataFrame([[1.0]], index=[1])
    tm.assert_frame_equal(res, expected)

