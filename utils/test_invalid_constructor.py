
def test_invalid_constructor(frame_or_series, w):
    # not valid

    c = frame_or_series(range(5)).rolling

    msg = "|".join(
        [
            "window must be an integer",
            "passed window foo is not compatible with a datetimelike index",
        ]
    )
    with pytest.raises(ValueError, match=msg):
        c(window=w)

    msg = "min_periods must be an integer"
    with pytest.raises(ValueError, match=msg):
        c(window=2, min_periods=w)

    msg = "center must be a boolean"
    with pytest.raises(ValueError, match=msg):
        c(window=2, min_periods=1, center=w)


def test_invalid_constructor(frame_or_series, w):
    # not valid
    pytest.importorskip("scipy")
    c = frame_or_series(range(5)).rolling
    with pytest.raises(ValueError, match="min_periods must be an integer"):
        c(win_type="boxcar", window=2, min_periods=w)
    with pytest.raises(ValueError, match="center must be a boolean"):
        c(win_type="boxcar", window=2, min_periods=1, center=w)

