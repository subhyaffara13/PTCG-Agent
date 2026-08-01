
def test_groupby_cumsum_timedelta64():
    # GH#46216 don't ignore is_datetimelike in libgroupby.group_cumsum
    dti = date_range("2016-01-01", periods=5, unit="ns")
    ser = Series(dti) - dti[0]
    ser[2] = pd.NaT

    df = DataFrame({"A": 1, "B": ser})
    gb = df.groupby("A")

    res = gb.cumsum(numeric_only=False, skipna=True)
    exp = DataFrame({"B": [ser[0], ser[1], pd.NaT, ser[4], ser[4] * 2]})
    tm.assert_frame_equal(res, exp)

    res = gb.cumsum(numeric_only=False, skipna=False)
    exp = DataFrame({"B": [ser[0], ser[1], pd.NaT, pd.NaT, pd.NaT]})
    tm.assert_frame_equal(res, exp)

