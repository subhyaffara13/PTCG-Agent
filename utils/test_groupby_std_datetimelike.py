
def test_groupby_std_datetimelike():
    # GH#48481
    tdi = pd.timedelta_range("1 Day", periods=10000, unit="ns")
    ser = Series(tdi)
    ser[::5] *= 2  # get different std for different groups

    df = ser.to_frame("A").copy()

    df["B"] = ser + Timestamp(0)
    df["C"] = ser + Timestamp(0, tz="UTC")
    df.iloc[-1] = pd.NaT  # last group includes NaTs

    gb = df.groupby(list(range(5)) * 2000)

    result = gb.std()

    # Note: this does not _exactly_ match what we would get if we did
    # [gb.get_group(i).std() for i in gb.groups]
    #  but it _does_ match the floating point error we get doing the
    #  same operation on int64 data xref GH#51332
    td1 = pd.Timedelta("2887 days 11:21:02.326710176")
    td4 = pd.Timedelta("2886 days 00:42:34.664668096")
    exp_ser = Series([td1 * 2, td1, td1, td1, td4], index=np.arange(5))
    expected = DataFrame({"A": exp_ser, "B": exp_ser, "C": exp_ser})
    tm.assert_frame_equal(result, expected)

