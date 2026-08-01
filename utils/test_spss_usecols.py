
def test_spss_usecols(datapath):
    # usecols must be list-like
    fname = datapath("io", "data", "spss", "labelled-num.sav")

    with pytest.raises(TypeError, match="usecols must be list-like."):
        pd.read_spss(fname, usecols="VAR00002")

