
def test_store_index_name_with_tz(temp_hdfstore):
    # GH 13884
    df = DataFrame({"A": [1, 2]})
    df.index = DatetimeIndex([1234567890123456787, 1234567890123456788])
    df.index = df.index.tz_localize("UTC")
    df.index.name = "foo"

    temp_hdfstore.put("frame", df, format="table")
    recons = temp_hdfstore["frame"]
    tm.assert_frame_equal(recons, df)

