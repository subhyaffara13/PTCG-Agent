
def test_consistent_win_type_freq(arg):
    # GH 15969
    pytest.importorskip("scipy")
    s = Series(range(1))
    with pytest.raises(ValueError, match="Invalid win_type freq"):
        s.rolling(arg, win_type="freq")

