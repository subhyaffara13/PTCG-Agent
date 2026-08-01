
def test_column_multiindex_existing(temp_hdfstore, using_infer_string):
    # appending multi-column on existing table (see GH 6167)

    index = MultiIndex.from_tuples(
        [("A", "a"), ("A", "b"), ("B", "a"), ("B", "b")], names=["first", "second"]
    )
    df = DataFrame(np.arange(12).reshape(3, 4), columns=index)
    temp_hdfstore.append("df2", df)
    temp_hdfstore.append("df2", df)

    tm.assert_frame_equal(temp_hdfstore["df2"], concat((df, df)))

