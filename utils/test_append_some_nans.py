
def test_append_some_nans(temp_hdfstore):
    df = DataFrame(
        {
            "A": Series(np.random.default_rng(2).standard_normal(20)).astype("int32"),
            "A1": np.random.default_rng(2).standard_normal(20),
            "A2": np.random.default_rng(2).standard_normal(20),
            "B": "foo",
            "C": "bar",
            "D": Timestamp("2001-01-01").as_unit("ns"),
            "E": Timestamp("2001-01-02").as_unit("ns"),
        },
        index=np.arange(20),
    )
    # some nans
    df.loc[0:15, ["A1", "B", "D", "E"]] = np.nan
    temp_hdfstore.append("df1", df[:10])
    temp_hdfstore.append("df1", df[10:])
    tm.assert_frame_equal(temp_hdfstore["df1"], df, check_index_type=True)

    # first column
    df1 = df.copy()
    df1["A1"] = np.nan
    temp_hdfstore.remove("df1")
    temp_hdfstore.append("df1", df1[:10])
    temp_hdfstore.append("df1", df1[10:])
    tm.assert_frame_equal(temp_hdfstore["df1"], df1, check_index_type=True)

    # 2nd column
    df2 = df.copy()
    df2["A2"] = np.nan
    temp_hdfstore.append("df2", df2[:10])
    temp_hdfstore.append("df2", df2[10:])
    tm.assert_frame_equal(temp_hdfstore["df2"], df2, check_index_type=True)

    # datetimes
    df3 = df.copy()
    df3["E"] = np.nan
    temp_hdfstore.append("df3", df3[:10])
    temp_hdfstore.append("df3", df3[10:])
    tm.assert_frame_equal(temp_hdfstore["df3"], df3, check_index_type=True)

