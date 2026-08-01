
def test_shift_disallow_freq_and_fill_value():
    # GH 53832
    data = {"a": [1, 2, 3, 4, 5, 6], "b": [0, 0, 0, 1, 1, 1]}
    df = DataFrame(data, index=date_range(start="20100101", periods=6))
    msg = "Passing a 'freq' together with a 'fill_value'"
    with pytest.raises(ValueError, match=msg):
        df.groupby(df.index).shift(periods=-2, freq="D", fill_value="1")

