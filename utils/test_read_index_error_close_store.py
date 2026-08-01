
def test_read_index_error_close_store(temp_h5_path):
    # GH 25766
    df = DataFrame({"A": [], "B": []}, index=[])
    df.to_hdf(temp_h5_path, key="k1")

    with pytest.raises(IndexError, match=r"list index out of range"):
        read_hdf(temp_h5_path, "k1", stop=0)

    # smoke test to test that file is properly closed after
    # read with IndexError before another write
    df.to_hdf(temp_h5_path, key="k1")

