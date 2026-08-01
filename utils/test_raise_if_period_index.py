
def test_raise_if_period_index():
    index = period_range(start="1/1/1990", periods=20, freq="M")
    msg = "Check the `freq` attribute instead of using infer_freq"

    with pytest.raises(TypeError, match=msg):
        frequencies.infer_freq(index)

