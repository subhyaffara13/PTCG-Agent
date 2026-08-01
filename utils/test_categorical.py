
def test_categorical(df_from_dict):
    df = df_from_dict(
        {"weekday": ["Mon", "Tue", "Mon", "Wed", "Mon", "Thu", "Fri", "Sat", "Sun"]},
        is_categorical=True,
    )

    with tm.assert_produces_warning(match="Interchange"):
        colX = df.__dataframe__().get_column_by_name("weekday")
    categorical = colX.describe_categorical
    assert isinstance(categorical["is_ordered"], bool)
    assert isinstance(categorical["is_dictionary"], bool)


def test_categorical(temp_hdfstore):
    # Basic
    s = Series(
        Categorical(
            ["a", "b", "b", "a", "a", "c"],
            categories=["a", "b", "c", "d"],
            ordered=False,
        )
    )
    temp_hdfstore.append("s", s, format="table")
    result = temp_hdfstore.select("s")
    tm.assert_series_equal(s, result)

    s = Series(
        Categorical(
            ["a", "b", "b", "a", "a", "c"],
            categories=["a", "b", "c", "d"],
            ordered=True,
        )
    )
    temp_hdfstore.append("s_ordered", s, format="table")
    result = temp_hdfstore.select("s_ordered")
    tm.assert_series_equal(s, result)

    df = DataFrame({"s": s, "vals": [1, 2, 3, 4, 5, 6]})
    temp_hdfstore.append("df", df, format="table")
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

    # Dtypes
    s = Series([1, 1, 2, 2, 3, 4, 5]).astype("category")
    temp_hdfstore.append("si", s)
    result = temp_hdfstore.select("si")
    tm.assert_series_equal(result, s)

    s = Series([1, 1, np.nan, 2, 3, 4, 5]).astype("category")
    temp_hdfstore.append("si2", s)
    result = temp_hdfstore.select("si2")
    tm.assert_series_equal(result, s)

    # Multiple
    df2 = df.copy()
    df2["s2"] = Series(list("abcdefg")).astype("category")
    temp_hdfstore.append("df2", df2)
    result = temp_hdfstore.select("df2")
    tm.assert_frame_equal(result, df2)

    # Make sure the metadata is OK
    info = temp_hdfstore.info()
    assert "/df2   " in info
    # df2._mgr.blocks[0] and df2._mgr.blocks[2] are Categorical
    assert "/df2/meta/values_block_0/meta" in info
    assert "/df2/meta/values_block_2/meta" in info

    # unordered
    s = Series(
        Categorical(
            ["a", "b", "b", "a", "a", "c"],
            categories=["a", "b", "c", "d"],
            ordered=False,
        )
    )
    temp_hdfstore.append("s2", s, format="table")
    result = temp_hdfstore.select("s2")
    tm.assert_series_equal(result, s)

    # Query
    temp_hdfstore.append("df3", df, data_columns=["s"])
    expected = df[df.s.isin(["b", "c"])]
    result = temp_hdfstore.select("df3", where=['s in ["b","c"]'])
    tm.assert_frame_equal(result, expected)

    expected = df[df.s.isin(["b", "c"])]
    result = temp_hdfstore.select("df3", where=['s = ["b","c"]'])
    tm.assert_frame_equal(result, expected)

    expected = df[df.s.isin(["d"])]
    result = temp_hdfstore.select("df3", where=['s in ["d"]'])
    tm.assert_frame_equal(result, expected)

    expected = df[df.s.isin(["f"])]
    result = temp_hdfstore.select("df3", where=['s in ["f"]'])
    tm.assert_frame_equal(result, expected)

    # Appending with same categories is ok
    temp_hdfstore.append("df3", df)

    df = concat([df, df])
    expected = df[df.s.isin(["b", "c"])]
    result = temp_hdfstore.select("df3", where=['s in ["b","c"]'])
    tm.assert_frame_equal(result, expected)

    # Appending must have the same categories
    df3 = df.copy()
    df3["s"] = df3["s"].cat.remove_unused_categories()

    msg = "cannot append a categorical with different categories to the existing"
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.append("df3", df3)

    # Remove, and make sure meta data is removed (its a recursive
    # removal so should be).
    result = temp_hdfstore.select("df3/meta/s/meta")
    assert result is not None
    temp_hdfstore.remove("df3")

    with pytest.raises(KeyError, match="'No object named df3/meta/s/meta in the file'"):
        temp_hdfstore.select("df3/meta/s/meta")

