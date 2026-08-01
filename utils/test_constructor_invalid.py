
def test_constructor_invalid(frame_or_series, w):
    # not valid

    c = frame_or_series(range(5)).expanding
    msg = "min_periods must be an integer"
    with pytest.raises(ValueError, match=msg):
        c(min_periods=w)

