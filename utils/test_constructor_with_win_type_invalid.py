
def test_constructor_with_win_type_invalid(frame_or_series):
    # GH 13383
    pytest.importorskip("scipy")
    c = frame_or_series(range(5)).rolling

    msg = "window must be an integer 0 or greater"

    with pytest.raises(ValueError, match=msg):
        c(-1, win_type="boxcar")

