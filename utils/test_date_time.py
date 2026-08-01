
def test_date_time(datapath):
    # Support of different SAS date/datetime formats (PR #15871)
    fname = datapath("io", "sas", "data", "datetime.sas7bdat")
    df = pd.read_sas(fname)
    fname = datapath("io", "sas", "data", "datetime.csv")
    df0 = pd.read_csv(
        fname, parse_dates=["Date1", "Date2", "DateTime", "DateTimeHi", "Taiw"]
    )
    # GH 19732: Timestamps imported from sas will incur floating point errors
    # See GH#56014 for discussion of the correct "expected" results
    #  We are really just testing that we are "close". This only seems to be
    #  an issue near the implementation bounds.

    df[df.columns[3]] = df.iloc[:, 3].dt.round("us")
    df0["Date1"] = df0["Date1"].astype("M8[s]")
    df0["Date2"] = df0["Date2"].astype("M8[s]")
    df0["DateTime"] = df0["DateTime"].astype("M8[ms]")
    df0["Taiw"] = df0["Taiw"].astype("M8[s]")

    res = df0["DateTimeHi"].astype("M8[us]").dt.round("ms")
    df0["DateTimeHi"] = res.astype("M8[ms]")

    if not IS64:
        # No good reason for this, just what we get on the CI
        df0.loc[0, "DateTimeHi"] += np.timedelta64(1, "ms")
        df0.loc[[2, 3], "DateTimeHi"] -= np.timedelta64(1, "ms")
    tm.assert_frame_equal(df, df0)

