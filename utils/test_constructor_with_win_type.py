
def test_constructor_with_win_type(frame_or_series, win_types):
    # GH 12669
    pytest.importorskip("scipy")
    c = frame_or_series(range(5)).rolling
    c(win_type=win_types, window=2)

