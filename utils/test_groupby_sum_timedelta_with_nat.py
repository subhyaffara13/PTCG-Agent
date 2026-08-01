
def test_groupby_sum_timedelta_with_nat():
    # GH#42659
    df = DataFrame(
        {
            "a": [1, 1, 2, 2],
            "b": [pd.Timedelta("1D"), pd.Timedelta("2D"), pd.Timedelta("3D"), pd.NaT],
        }
    )
    td3 = pd.Timedelta(days=3).as_unit("us")

    gb = df.groupby("a")

    res = gb.sum()
    expected = DataFrame({"b": [td3, td3]}, index=pd.Index([1, 2], name="a"))
    tm.assert_frame_equal(res, expected)

    res = gb["b"].sum()
    tm.assert_series_equal(res, expected["b"])

    res = gb["b"].sum(min_count=2)
    expected = Series([td3, pd.NaT], dtype="m8[us]", name="b", index=expected.index)
    tm.assert_series_equal(res, expected)

