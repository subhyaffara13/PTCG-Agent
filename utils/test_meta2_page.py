
def test_meta2_page(datapath):
    # GH 35545
    fname = datapath("io", "sas", "data", "test_meta2_page.sas7bdat")
    df = pd.read_sas(fname)
    assert len(df) == 1000

