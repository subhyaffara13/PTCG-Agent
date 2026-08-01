
def test_fillna_non_scalar_raises(data_missing):
    msg = "can only insert Interval objects and NA into an IntervalArray"
    with pytest.raises(TypeError, match=msg):
        data_missing.fillna([1, 1])

