
def test_many_columns(datapath):
    # Test for looking for column information in more places (PR #22628)
    fname = datapath("io", "sas", "data", "many_columns.sas7bdat")

    df = pd.read_sas(fname, encoding="latin-1")

    fname = datapath("io", "sas", "data", "many_columns.csv")
    df0 = pd.read_csv(fname, encoding="latin-1")
    tm.assert_frame_equal(df, df0)

