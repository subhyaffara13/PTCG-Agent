
def test_cut_not_1d_arg(arg, cut_func):
    msg = "Input array must be 1 dimensional"
    with pytest.raises(ValueError, match=msg):
        cut_func(arg, 2)

