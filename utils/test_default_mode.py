
def test_default_mode(temp_h5_path, using_infer_string):
    # read_hdf uses default mode
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=date_range("2000-01-01", periods=10, freq="B"),
    )
    df.to_hdf(temp_h5_path, key="df", mode="w")
    result = read_hdf(temp_h5_path, "df")
    expected = df.copy()
    if using_infer_string:
        expected.columns = expected.columns.astype("str")
    tm.assert_frame_equal(result, expected)

