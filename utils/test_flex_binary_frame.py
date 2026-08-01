
def test_flex_binary_frame(method, frame):
    series = frame[1]

    res = getattr(series.rolling(window=10), method)(frame)
    res2 = getattr(frame.rolling(window=10), method)(series)
    exp = frame.apply(lambda x: getattr(series.rolling(window=10), method)(x))

    tm.assert_frame_equal(res, exp)
    tm.assert_frame_equal(res2, exp)

    frame2 = DataFrame(
        np.random.default_rng(2).standard_normal(frame.shape),
        index=frame.index,
        columns=frame.columns,
    )

    res3 = getattr(frame.rolling(window=10), method)(frame2)
    res3.columns = Index(list(res3.columns))
    exp = DataFrame(
        {k: getattr(frame[k].rolling(window=10), method)(frame2[k]) for k in frame}
    )
    tm.assert_frame_equal(res3, exp)

