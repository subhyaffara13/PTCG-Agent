
def test_store_hierarchical(
    temp_h5_path, using_infer_string, multiindex_dataframe_random_data
):
    frame = multiindex_dataframe_random_data

    _check_roundtrip(frame, tm.assert_frame_equal, path=temp_h5_path)
    _check_roundtrip(frame.T, tm.assert_frame_equal, path=temp_h5_path)
    _check_roundtrip(frame["A"], tm.assert_series_equal, path=temp_h5_path)

    # check that the names are stored
    with HDFStore(temp_h5_path) as store:
        store["frame"] = frame
        recons = store["frame"]
        tm.assert_frame_equal(recons, frame)

