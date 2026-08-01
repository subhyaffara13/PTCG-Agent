
def test_group_shift_with_multiple_periods_and_both_fill_and_freq_deprecated():
    # GH#44424
    df = DataFrame(
        {"a": [1, 2, 3, 4, 5], "b": [True, True, False, False, True]},
        index=date_range("1/1/2000", periods=5, freq="h"),
    )
    msg = "Passing a 'freq' together with a 'fill_value'"
    with pytest.raises(ValueError, match=msg):
        df.groupby("b")[["a"]].shift([1, 2], fill_value=1, freq="h")

