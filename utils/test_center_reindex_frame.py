
def test_center_reindex_frame(raw):
    # shifter index
    frame = DataFrame(range(100), index=date_range("2020-01-01", freq="D", periods=100))
    s = [f"x{x:d}" for x in range(12)]
    minp = 10

    frame_xp = (
        frame.reindex(list(frame.index) + s)
        .rolling(window=25, min_periods=minp)
        .apply(f, raw=raw)
        .shift(-12)
        .reindex(frame.index)
    )
    frame_rs = frame.rolling(window=25, min_periods=minp, center=True).apply(f, raw=raw)
    tm.assert_frame_equal(frame_xp, frame_rs)


def test_center_reindex_frame(frame, roll_func, kwargs, minp, fill_value):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    frame_xp = (
        getattr(
            frame.reindex(list(frame.index) + s).rolling(window=25, min_periods=minp),
            roll_func,
        )(**kwargs)
        .shift(-12)
        .reindex(frame.index)
    )
    frame_rs = getattr(
        frame.rolling(window=25, min_periods=minp, center=True), roll_func
    )(**kwargs)
    if fill_value is not None:
        frame_xp = frame_xp.fillna(fill_value)
    tm.assert_frame_equal(frame_xp, frame_rs)


def test_center_reindex_frame(frame, q):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    frame_xp = (
        frame.reindex(list(frame.index) + s)
        .rolling(window=25)
        .quantile(q)
        .shift(-12)
        .reindex(frame.index)
    )
    frame_rs = frame.rolling(window=25, center=True).quantile(q)
    tm.assert_frame_equal(frame_xp, frame_rs)


def test_center_reindex_frame(frame, roll_func):
    # shifter index
    s = [f"x{x:d}" for x in range(12)]

    frame_xp = (
        getattr(
            frame.reindex(list(frame.index) + s).rolling(window=25),
            roll_func,
        )()
        .shift(-12)
        .reindex(frame.index)
    )
    frame_rs = getattr(frame.rolling(window=25, center=True), roll_func)()
    tm.assert_frame_equal(frame_xp, frame_rs)

