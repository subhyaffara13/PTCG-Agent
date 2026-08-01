
def test_read_hdf_errors(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )

    msg = r"File [\S]* does not exist"
    with pytest.raises(OSError, match=msg):
        read_hdf(f"{uuid.uuid4()}.h5", "key")

    df.to_hdf(temp_h5_path, key="df")
    store = HDFStore(temp_h5_path, mode="r")
    store.close()

    msg = "The HDFStore must be open for reading."
    with pytest.raises(OSError, match=msg):
        read_hdf(store, "df")

