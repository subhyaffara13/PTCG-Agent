
def test_no_1d_support_in_init(spcreator):
    with pytest.raises(ValueError, match="arrays don't support 1D input"):
        spcreator([0, 1, 2, 3])

