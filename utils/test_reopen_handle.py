
def test_reopen_handle(temp_h5_path):
    store = HDFStore(temp_h5_path, mode="a")
    store["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )

    msg = (
        r"Re-opening the file \[[\S]*\] with mode \[a\] will delete the "
        "current file!"
    )
    # invalid mode change
    with pytest.raises(PossibleDataLossError, match=msg):
        store.open("w")

    store.close()
    assert not store.is_open

    # truncation ok here
    store.open("w")
    assert store.is_open
    assert len(store) == 0
    store.close()
    assert not store.is_open

    store = HDFStore(temp_h5_path, mode="a")
    store["a"] = Series(
        np.arange(10, dtype=np.float64), index=date_range("2020-01-01", periods=10)
    )

    # reopen as read
    store.open("r")
    assert store.is_open
    assert len(store) == 1
    assert store._mode == "r"
    store.close()
    assert not store.is_open

    # reopen as append
    store.open("a")
    assert store.is_open
    assert len(store) == 1
    assert store._mode == "a"
    store.close()
    assert not store.is_open

    # reopen as append (again)
    store.open("a")
    assert store.is_open
    assert len(store) == 1
    assert store._mode == "a"
    store.close()
    assert not store.is_open

