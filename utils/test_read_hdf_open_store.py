
def test_read_hdf_open_store(temp_h5_path, using_infer_string):
    # GH10330
    # No check for non-string path_or-buf, and no test of open store
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )
    df.index.name = "letters"
    df = df.set_index(keys="E", append=True)

    df.to_hdf(temp_h5_path, key="df", mode="w")
    direct = read_hdf(temp_h5_path, "df")
    with HDFStore(temp_h5_path, mode="r") as store:
        indirect = read_hdf(store, "df")
        tm.assert_frame_equal(direct, indirect)
        assert store.is_open

