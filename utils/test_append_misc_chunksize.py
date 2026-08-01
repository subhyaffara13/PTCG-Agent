
def test_append_misc_chunksize(temp_hdfstore, chunksize):
    # more chunksize in append tests
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    df["string"] = "foo"
    df["float322"] = 1.0
    df["float322"] = df["float322"].astype("float32")
    df["bool"] = df["float322"] > 0
    df["time1"] = Timestamp("20130101").as_unit("ns")
    df["time2"] = Timestamp("20130102").as_unit("ns")
    temp_hdfstore.append("obj", df, chunksize=chunksize)
    result = temp_hdfstore.select("obj")
    tm.assert_frame_equal(result, df)

