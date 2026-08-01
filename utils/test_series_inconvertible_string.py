
def test_series_inconvertible_string(using_infer_string):
    # see gh-6407
    if using_infer_string:
        msg = "cannot infer freq from"

        with pytest.raises(TypeError, match=msg):
            frequencies.infer_freq(Series(["foo", "bar"]))
    else:
        msg = "Unknown datetime string format"

        with pytest.raises(ValueError, match=msg):
            frequencies.infer_freq(Series(["foo", "bar"]))

