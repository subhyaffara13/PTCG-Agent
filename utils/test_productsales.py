
def test_productsales(datapath):
    fname = datapath("io", "sas", "data", "productsales.sas7bdat")
    df = pd.read_sas(fname, encoding="utf-8")
    fname = datapath("io", "sas", "data", "productsales.csv")
    df0 = pd.read_csv(fname, parse_dates=["MONTH"])
    vn = ["ACTUAL", "PREDICT", "QUARTER", "YEAR"]
    df0[vn] = df0[vn].astype(np.float64)

    df0["MONTH"] = df0["MONTH"].astype("M8[s]")
    tm.assert_frame_equal(df, df0)

