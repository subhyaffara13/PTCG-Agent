
def test_read_hdf_series_mode_r(temp_h5_path, format):
    # GH 16583
    # Tests that reading a Series saved to an HDF file
    # still works if a mode='r' argument is supplied
    series = Series(range(10), dtype=np.float64)
    series.to_hdf(temp_h5_path, key="data", format=format)
    result = read_hdf(temp_h5_path, key="data", mode="r")
    tm.assert_series_equal(result, series)

