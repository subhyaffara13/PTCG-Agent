
def test_append_misc_empty_frame(temp_hdfstore):
    # empty frame, GH4273
    # 0 len
    df_empty = DataFrame(columns=list("ABC"))
    temp_hdfstore.append("df", df_empty)
    with pytest.raises(KeyError, match="'No object named df in the file'"):
        temp_hdfstore.select("df")

    # repeated append of 0/non-zero frames
    df = DataFrame(np.random.default_rng(2).random((10, 3)), columns=list("ABC"))
    temp_hdfstore.append("df", df)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)
    temp_hdfstore.append("df", df_empty)
    tm.assert_frame_equal(temp_hdfstore.select("df"), df)

    # store
    df = DataFrame(columns=list("ABC"))
    temp_hdfstore.put("df2", df)
    tm.assert_frame_equal(temp_hdfstore.select("df2"), df)

