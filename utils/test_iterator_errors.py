
def test_iterator_errors(datapath, chunksize):
    dta_file = datapath("io", "data", "stata", "stata-dta-partially-labeled.dta")
    with pytest.raises(ValueError, match="chunksize must be a positive"):
        with StataReader(dta_file, chunksize=chunksize):
            pass

