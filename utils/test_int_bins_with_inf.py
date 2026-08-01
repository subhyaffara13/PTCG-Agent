
def test_int_bins_with_inf(data):
    # GH 24314
    msg = "cannot specify integer `bins` when input data contains infinity"
    with pytest.raises(ValueError, match=msg):
        cut(data, bins=3)

