
def test_select_iterator3(temp_h5_path):
    df = DataFrame(
        np.random.default_rng(2).standard_normal((10, 4)),
        columns=Index(list("ABCD")),
        index=date_range("2000-01-01", periods=10, freq="B", unit="ns"),
    )
    df.to_hdf(temp_h5_path, key="df", format="table")

    results = list(read_hdf(temp_h5_path, "df", chunksize=2))
    result = concat(results)

    assert len(results) == 5
    tm.assert_frame_equal(result, df)
    tm.assert_frame_equal(result, read_hdf(temp_h5_path, "df"))

