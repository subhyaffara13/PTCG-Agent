
def test_read_missing_key_close_store(temp_h5_path):
    # GH 25766
    df = DataFrame({"a": range(2), "b": range(2)})
    df.to_hdf(temp_h5_path, key="k1")

    with pytest.raises(KeyError, match="'No object named k2 in the file'"):
        read_hdf(temp_h5_path, "k2")

    # smoke test to test that file is properly closed after
    # read with KeyError before another write
    df.to_hdf(temp_h5_path, key="k2")

