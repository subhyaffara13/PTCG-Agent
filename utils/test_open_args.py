
def test_open_args(using_infer_string):
    not_written = f"{uuid.uuid4()}.h5"
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )

    # create an in memory store
    store = HDFStore(
        not_written, mode="a", driver="H5FD_CORE", driver_core_backing_store=0
    )
    store["df"] = df
    store.append("df2", df)

    expected = df.copy()
    if using_infer_string:
        expected.index = expected.index.astype("str")
        expected.columns = expected.columns.astype("str")

    tm.assert_frame_equal(store["df"], expected)
    tm.assert_frame_equal(store["df2"], expected)

    store.close()

    # the file should not have actually been written
    assert not os.path.exists(not_written)

