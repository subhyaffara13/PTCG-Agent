
def test_column_multiindex_non_index_axes(temp_hdfstore, using_infer_string):
    df = DataFrame(np.arange(12).reshape(3, 4), columns=Index(list("ABCD"), name="foo"))
    expected = df.set_axis(df.index.to_numpy())

    temp_hdfstore.put("df1", df, format="table")
    tm.assert_frame_equal(
        temp_hdfstore["df1"], expected, check_index_type=True, check_column_type=True
    )

