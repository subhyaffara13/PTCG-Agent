
def test_multiple_open_close(temp_h5_path):
    # gh-4409: open & close multiple times

    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df.to_hdf(temp_h5_path, key="df", mode="w", format="table")

    # single
    store = HDFStore(temp_h5_path)
    assert "CLOSED" not in store.info()
    assert store.is_open

    store.close()
    assert "CLOSED" in store.info()
    assert not store.is_open

    if pytables._table_file_open_policy_is_strict:
        # multiples
        store1 = HDFStore(temp_h5_path)
        msg = (
            r"The file [\S]* is already opened\.  Please close it before "
            r"reopening in write mode\."
        )
        with pytest.raises(ValueError, match=msg):
            HDFStore(temp_h5_path)

        store1.close()
    else:
        # multiples
        store1 = HDFStore(temp_h5_path)
        store2 = HDFStore(temp_h5_path)

        assert "CLOSED" not in store1.info()
        assert "CLOSED" not in store2.info()
        assert store1.is_open
        assert store2.is_open

        store1.close()
        assert "CLOSED" in store1.info()
        assert not store1.is_open
        assert "CLOSED" not in store2.info()
        assert store2.is_open

        store2.close()
        assert "CLOSED" in store1.info()
        assert "CLOSED" in store2.info()
        assert not store1.is_open
        assert not store2.is_open

        # nested close
        store = HDFStore(temp_h5_path, mode="w")
        store.append("df", df)

        store2 = HDFStore(temp_h5_path)
        store2.append("df2", df)
        store2.close()
        assert "CLOSED" in store2.info()
        assert not store2.is_open

        store.close()
        assert "CLOSED" in store.info()
        assert not store.is_open

        # double closing
        store = HDFStore(temp_h5_path, mode="w")
        store.append("df", df)

        store2 = HDFStore(temp_h5_path)
        store.close()
        assert "CLOSED" in store.info()
        assert not store.is_open

        store2.close()
        assert "CLOSED" in store2.info()
        assert not store2.is_open

    # ops on a closed store
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df.to_hdf(temp_h5_path, key="df", mode="w", format="table")

    store = HDFStore(temp_h5_path)
    store.close()

    msg = r"[\S]* file is not open!"
    with pytest.raises(ClosedFileError, match=msg):
        store.keys()

    with pytest.raises(ClosedFileError, match=msg):
        "df" in store

    with pytest.raises(ClosedFileError, match=msg):
        len(store)

    with pytest.raises(ClosedFileError, match=msg):
        store["df"]

    with pytest.raises(ClosedFileError, match=msg):
        store.select("df")

    with pytest.raises(ClosedFileError, match=msg):
        store.get("df")

    with pytest.raises(ClosedFileError, match=msg):
        store.append("df2", df)

    with pytest.raises(ClosedFileError, match=msg):
        store.put("df3", df)

    with pytest.raises(ClosedFileError, match=msg):
        store.get_storer("df2")

    with pytest.raises(ClosedFileError, match=msg):
        store.remove("df2")

    with pytest.raises(ClosedFileError, match=msg):
        store.select("df")

    msg = "'HDFStore' object has no attribute 'df'"
    with pytest.raises(AttributeError, match=msg):
        store.df

