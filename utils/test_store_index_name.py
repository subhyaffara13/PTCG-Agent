
def test_store_index_name(temp_hdfstore):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    df.index.name = "foo"

    temp_hdfstore["frame"] = df
    recons = temp_hdfstore["frame"]
    tm.assert_frame_equal(recons, df)

