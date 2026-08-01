
def test_append_misc(temp_hdfstore):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    temp_hdfstore.append("df", df, chunksize=1)
    result = temp_hdfstore.select("df")
    tm.assert_frame_equal(result, df)

    temp_hdfstore.append("df1", df, expectedrows=10)
    result = temp_hdfstore.select("df1")
    tm.assert_frame_equal(result, df)

