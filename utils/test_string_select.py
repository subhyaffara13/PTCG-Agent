
def test_string_select(temp_hdfstore):
    # GH 2973
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )

    # test string ==/!=
    df["x"] = "none"
    df.loc[df.index[2:7], "x"] = ""

    temp_hdfstore.append("df", df, data_columns=["x"])

    result = temp_hdfstore.select("df", "x=none")
    expected = df[df.x == "none"]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df", "x!=none")
    expected = df[df.x != "none"]
    tm.assert_frame_equal(result, expected)

    df2 = df.copy()
    df2.loc[df2.x == "", "x"] = np.nan

    temp_hdfstore.append("df2", df2, data_columns=["x"])
    result = temp_hdfstore.select("df2", "x!=none")
    expected = df2[isna(df2.x)]
    tm.assert_frame_equal(result, expected)

    # int ==/!=
    df["int"] = 1
    df.loc[df.index[2:7], "int"] = 2

    temp_hdfstore.append("df3", df, data_columns=["int"])

    result = temp_hdfstore.select("df3", "int=2")
    expected = df[df.int == 2]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df3", "int!=2")
    expected = df[df.int != 2]
    tm.assert_frame_equal(result, expected)

