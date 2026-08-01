
def test_encoding_infer(datapath):
    fname = datapath("io", "sas", "data", "test1.sas7bdat")

    with pd.read_sas(fname, encoding="infer", iterator=True) as df1_reader:
        # check: is encoding inferred correctly from file
        assert df1_reader.inferred_encoding == "cp1252"
        df1 = df1_reader.read()

    with pd.read_sas(fname, encoding="cp1252", iterator=True) as df2_reader:
        df2 = df2_reader.read()

    # check: reader reads correct information
    tm.assert_frame_equal(df1, df2)

