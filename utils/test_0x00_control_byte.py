
def test_0x00_control_byte(datapath):
    # GH 47099
    fname = datapath("io", "sas", "data", "0x00controlbyte.sas7bdat.bz2")
    df = next(pd.read_sas(fname, chunksize=11_000))
    assert df.shape == (11_000, 20)

