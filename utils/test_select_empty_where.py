
def test_select_empty_where(temp_hdfstore, where):
    # GH26610

    df = DataFrame([1, 2, 3])
    temp_hdfstore.put("df", df, "t")
    result = read_hdf(temp_hdfstore, "df", where=where)
    tm.assert_frame_equal(result, df)

