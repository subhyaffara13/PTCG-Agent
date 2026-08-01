
def test_frame_select_complex(temp_hdfstore):
    # select via complex criteria

    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df["string"] = "foo"
    df.loc[df.index[0:4], "string"] = "bar"

    temp_hdfstore.put("df", df, format="table", data_columns=["string"])

    # empty
    result = temp_hdfstore.select("df", 'index>df.index[3] & string="bar"')
    expected = df.loc[(df.index > df.index[3]) & (df.string == "bar")]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df", 'index>df.index[3] & string="foo"')
    expected = df.loc[(df.index > df.index[3]) & (df.string == "foo")]
    tm.assert_frame_equal(result, expected)

    # or
    result = temp_hdfstore.select("df", 'index>df.index[3] | string="bar"')
    expected = df.loc[(df.index > df.index[3]) | (df.string == "bar")]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select(
        "df", '(index>df.index[3] & index<=df.index[6]) | string="bar"'
    )
    expected = df.loc[
        ((df.index > df.index[3]) & (df.index <= df.index[6])) | (df.string == "bar")
    ]
    tm.assert_frame_equal(result, expected)

    # invert
    result = temp_hdfstore.select("df", 'string!="bar"')
    expected = df.loc[df.string != "bar"]
    tm.assert_frame_equal(result, expected)

    # invert not implemented in numexpr :(
    msg = "cannot use an invert condition when passing to numexpr"
    with pytest.raises(NotImplementedError, match=msg):
        temp_hdfstore.select("df", '~(string="bar")')

    # invert ok for filters
    result = temp_hdfstore.select("df", "~(columns=['A','B'])")
    expected = df.loc[:, df.columns.difference(["A", "B"])]
    tm.assert_frame_equal(result, expected)

    # in
    result = temp_hdfstore.select("df", "index>df.index[3] & columns in ['A','B']")
    expected = df.loc[df.index > df.index[3]].reindex(columns=["A", "B"])
    tm.assert_frame_equal(result, expected)

