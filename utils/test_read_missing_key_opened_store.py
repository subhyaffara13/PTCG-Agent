
def test_read_missing_key_opened_store(temp_h5_path):
    # GH 28699
    df = DataFrame({"a": range(2), "b": range(2)})
    df.to_hdf(temp_h5_path, key="k1")

    with HDFStore(temp_h5_path, "r") as store:
        with pytest.raises(KeyError, match="'No object named k2 in the file'"):
            read_hdf(store, "k2")

        # Test that the file is still open after a KeyError and that we can
        # still read from it.
        read_hdf(store, "k1")

