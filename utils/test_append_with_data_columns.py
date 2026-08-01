
def test_append_with_data_columns(temp_hdfstore):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df.iloc[0, df.columns.get_loc("B")] = 1.0
    temp_hdfstore.append("df", df[:2], data_columns=["B"])
    temp_hdfstore.append("df", df[2:])
    tm.assert_frame_equal(temp_hdfstore["df"], df)

    # check that we have indices created
    assert temp_hdfstore._handle.root.df.table.cols.index.is_indexed is True
    assert temp_hdfstore._handle.root.df.table.cols.B.is_indexed is True

    # data column searching
    result = temp_hdfstore.select("df", "B>0")
    expected = df[df.B > 0]
    tm.assert_frame_equal(result, expected)

    # data column searching (with an indexable and a data_columns)
    result = temp_hdfstore.select("df", "B>0 and index>df.index[3]")
    df_new = df.reindex(index=df.index[4:])
    expected = df_new[df_new.B > 0]
    tm.assert_frame_equal(result, expected)

    # data column selection with a string data_column
    df_new = df.copy()
    df_new["string"] = "foo"
    df_new.loc[df_new.index[1:4], "string"] = np.nan
    df_new.loc[df_new.index[5:6], "string"] = "bar"
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df_new, data_columns=["string"])
    result = temp_hdfstore.select("df", "string='foo'")
    expected = df_new[df_new.string == "foo"]
    tm.assert_frame_equal(result, expected)

    # using min_itemsize and a data column
    def check_col(key, name, size):
        assert (
            getattr(temp_hdfstore.get_storer(key).table.description, name).itemsize
            == size
        )

    temp_hdfstore.remove("df")
    temp_hdfstore.append(
        "df", df_new, data_columns=["string"], min_itemsize={"string": 30}
    )
    check_col("df", "string", 30)
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df_new, data_columns=["string"], min_itemsize=30)
    check_col("df", "string", 30)
    temp_hdfstore.remove("df")
    temp_hdfstore.append(
        "df", df_new, data_columns=["string"], min_itemsize={"values": 30}
    )
    check_col("df", "string", 30)

    df_new["string2"] = "foobarbah"
    df_new["string_block1"] = "foobarbah1"
    df_new["string_block2"] = "foobarbah2"
    temp_hdfstore.remove("df")
    temp_hdfstore.append(
        "df",
        df_new,
        data_columns=["string", "string2"],
        min_itemsize={"string": 30, "string2": 40, "values": 50},
    )
    check_col("df", "string", 30)
    check_col("df", "string2", 40)
    check_col("df", "values_block_1", 50)

    # multiple data columns
    df_new = df.copy()
    df_new.iloc[0, df_new.columns.get_loc("A")] = 1.0
    df_new.iloc[0, df_new.columns.get_loc("B")] = -1.0
    df_new["string"] = "foo"

    sl = df_new.columns.get_loc("string")
    df_new.iloc[1:4, sl] = np.nan
    df_new.iloc[5:6, sl] = "bar"

    df_new["string2"] = "foo"
    sl = df_new.columns.get_loc("string2")
    df_new.iloc[2:5, sl] = np.nan
    df_new.iloc[7:8, sl] = "bar"
    temp_hdfstore.remove("df")
    temp_hdfstore.append("df", df_new, data_columns=["A", "B", "string", "string2"])
    result = temp_hdfstore.select(
        "df", "string='foo' and string2='foo' and A>0 and B<0"
    )
    expected = df_new[
        (df_new.string == "foo")
        & (df_new.string2 == "foo")
        & (df_new.A > 0)
        & (df_new.B < 0)
    ]
    tm.assert_frame_equal(result, expected, check_freq=False)
    # FIXME: 2020-05-07 freq check randomly fails in the CI

    # yield an empty frame
    result = temp_hdfstore.select("df", "string='foo' and string2='cool'")
    expected = df_new[(df_new.string == "foo") & (df_new.string2 == "cool")]
    tm.assert_frame_equal(result, expected)

    # doc example
    df_dc = df.copy()
    df_dc["string"] = "foo"
    df_dc.loc[df_dc.index[4:6], "string"] = np.nan
    df_dc.loc[df_dc.index[7:9], "string"] = "bar"
    df_dc["string2"] = "cool"
    df_dc["datetime"] = Timestamp("20010102").as_unit("ns")
    df_dc.loc[df_dc.index[3:5], ["A", "B", "datetime"]] = np.nan

    temp_hdfstore.append(
        "df_dc", df_dc, data_columns=["B", "C", "string", "string2", "datetime"]
    )
    result = temp_hdfstore.select("df_dc", "B>0")

    expected = df_dc[df_dc.B > 0]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df_dc", ["B > 0", "C > 0", "string == foo"])
    expected = df_dc[(df_dc.B > 0) & (df_dc.C > 0) & (df_dc.string == "foo")]
    tm.assert_frame_equal(result, expected, check_freq=False)
    # FIXME: 2020-12-07 intermittent build failures here with freq of
    #  None instead of BDay(4)

    # doc example part 2

    index = date_range("1/1/2000", periods=8)
    df_dc = DataFrame(
        np.random.default_rng(2).standard_normal((8, 3)),
        index=index,
        columns=["A", "B", "C"],
    )
    df_dc["string"] = "foo"
    df_dc.loc[df_dc.index[4:6], "string"] = np.nan
    df_dc.loc[df_dc.index[7:9], "string"] = "bar"
    df_dc[["B", "C"]] = df_dc[["B", "C"]].abs()
    df_dc["string2"] = "cool"

    # on-disk operations
    temp_hdfstore.remove("df_dc")
    temp_hdfstore.append("df_dc", df_dc, data_columns=["B", "C", "string", "string2"])

    result = temp_hdfstore.select("df_dc", "B>0")
    expected = df_dc[df_dc.B > 0]
    tm.assert_frame_equal(result, expected)

    result = temp_hdfstore.select("df_dc", ["B > 0", "C > 0", 'string == "foo"'])
    expected = df_dc[(df_dc.B > 0) & (df_dc.C > 0) & (df_dc.string == "foo")]
    tm.assert_frame_equal(result, expected)

