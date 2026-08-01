
def test_groupby_timedelta_median():
    # issue 57926
    expected = Series(data=Timedelta("1D"), index=["foo"], dtype="m8[us]")
    df = DataFrame({"label": ["foo", "foo"], "timedelta": [pd.NaT, Timedelta("1D")]})
    gb = df.groupby("label")["timedelta"]
    actual = gb.median()
    tm.assert_series_equal(actual, expected, check_names=False)

