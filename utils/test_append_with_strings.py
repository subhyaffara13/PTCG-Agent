
def test_append_with_strings(temp_hdfstore):
    def check_col(key, name, size):
        assert (
            getattr(temp_hdfstore.get_storer(key).table.description, name).itemsize
            == size
        )

    # avoid truncation on elements
    df = DataFrame([[123, "asdqwerty"], [345, "dggnhebbsdfbdfb"]])
    temp_hdfstore.append("df_big", df)
    tm.assert_frame_equal(temp_hdfstore.select("df_big"), df)
    check_col("df_big", "values_block_1", 15)

    # appending smaller string ok
    df2 = DataFrame([[124, "asdqy"], [346, "dggnhefbdfb"]])
    temp_hdfstore.append("df_big", df2)
    expected = concat([df, df2])
    tm.assert_frame_equal(temp_hdfstore.select("df_big"), expected)
    check_col("df_big", "values_block_1", 15)

    # avoid truncation on elements
    df = DataFrame([[123, "asdqwerty"], [345, "dggnhebbsdfbdfb"]])
    temp_hdfstore.append("df_big2", df, min_itemsize={"values": 50})
    tm.assert_frame_equal(temp_hdfstore.select("df_big2"), df)
    check_col("df_big2", "values_block_1", 50)

    # bigger string on next append
    temp_hdfstore.append("df_new", df)
    df_new = DataFrame([[124, "abcdefqhij"], [346, "abcdefghijklmnopqrtsuvwxyz"]])
    msg = (
        r"Trying to store a string with len \[26\] in "
        r"\[values_block_1\] column but\n"
        r"this column has a limit of \[15\]!\n"
        "Consider using min_itemsize to preset the sizes on these "
        "columns"
    )
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df_new", df_new)

    # min_itemsize on Series index (GH 11412)
    df = DataFrame(
        {
            "A": [0.0, 1.0, 2.0, 3.0, 4.0],
            "B": [0.0, 1.0, 0.0, 1.0, 0.0],
            "C": Index(["foo1", "foo2", "foo3", "foo4", "foo5"]),
            "D": date_range("20130101", periods=5),
        }
    ).set_index("C")
    temp_hdfstore.append("ss", df["B"], min_itemsize={"index": 4})
    tm.assert_series_equal(temp_hdfstore.select("ss"), df["B"])

    # same as above, with data_columns=True
    temp_hdfstore.append("ss2", df["B"], data_columns=True, min_itemsize={"index": 4})
    tm.assert_series_equal(temp_hdfstore.select("ss2"), df["B"])

    # min_itemsize in index without appending (GH 10381)
    temp_hdfstore.put("ss3", df, format="table", min_itemsize={"index": 6})
    # just make sure there is a longer string:
    df2 = df.copy().reset_index().assign(C="longer").set_index("C")
    temp_hdfstore.append("ss3", df2)
    tm.assert_frame_equal(temp_hdfstore.select("ss3"), concat([df, df2]))

    # same as above, with a Series
    temp_hdfstore.put("ss4", df["B"], format="table", min_itemsize={"index": 6})
    temp_hdfstore.append("ss4", df2["B"])
    tm.assert_series_equal(temp_hdfstore.select("ss4"), concat([df["B"], df2["B"]]))

    # with nans
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df["string"] = "foo"
    df.loc[df.index[1:4], "string"] = np.nan
    df["string2"] = "bar"
    df.loc[df.index[4:8], "string2"] = np.nan
    df["string3"] = "bah"
    df.loc[df.index[1:], "string3"] = np.nan
    temp_hdfstore.append("df", df)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

