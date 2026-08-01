
def test_store_bool_index(temp_h5_path):
    # GH#48667
    df = DataFrame([[1]], columns=[True], index=Index([False], dtype="bool"))
    expected = df.copy()

    # # Test to make sure defaults are to not drop.
    # # Corresponding to Issue 9382
    df.to_hdf(temp_h5_path, key="a")
    result = read_hdf(temp_h5_path, "a")
    tm.assert_frame_equal(expected, result)

