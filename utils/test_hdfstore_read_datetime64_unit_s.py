
def test_hdfstore_read_datetime64_unit_s(temp_hdfstore):
    # GH 59004
    df_s = DataFrame(["2001-01-01", "2002-02-02"], dtype="datetime64[s]")
    temp_hdfstore.put("df_s", df_s)
    df_fromstore = temp_hdfstore.get("df_s")
    tm.assert_frame_equal(df_s, df_fromstore)

