
def test_column_multiindex(temp_hdfstore, using_infer_string):
    # GH 4710
    # recreate multi-indexes properly

    index = MultiIndex.from_tuples(
        [("A", "a"), ("A", "b"), ("B", "a"), ("B", "b")], names=["first", "second"]
    )
    df = DataFrame(np.arange(12).reshape(3, 4), columns=index)
    expected = df.set_axis(df.index.to_numpy())

    temp_hdfstore.put("df", df)
    tm.assert_frame_equal(
        temp_hdfstore["df"], expected, check_index_type=True, check_column_type=True
    )

    temp_hdfstore.put("df1", df, format="table")
    tm.assert_frame_equal(
        temp_hdfstore["df1"], expected, check_index_type=True, check_column_type=True
    )

    msg = re.escape("cannot use a multi-index on axis [1] with data_columns ['A']")
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.put("df2", df, format="table", data_columns=["A"])
    msg = re.escape("cannot use a multi-index on axis [1] with data_columns True")
    with pytest.raises(ValueError, match=msg):
        temp_hdfstore.put("df3", df, format="table", data_columns=True)

