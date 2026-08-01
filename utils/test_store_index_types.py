
def test_store_index_types(temp_hdfstore, format, index):
    # GH5386
    # test storing various index types
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 2)),
        columns=list("AB"),
        index=index,
    )
    temp_hdfstore.put("df", df, format=format)
    tm.assert_frame_equal(df, temp_hdfstore["df"])

