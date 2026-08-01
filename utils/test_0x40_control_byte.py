
def test_0x40_control_byte(datapath):
    # GH 31243
    fname = datapath("io", "sas", "data", "0x40controlbyte.sas7bdat")
    df = pd.read_sas(fname, encoding="ascii")
    fname = datapath("io", "sas", "data", "0x40controlbyte.csv")
    df0 = pd.read_csv(fname, dtype="str")
    tm.assert_frame_equal(df, df0)

