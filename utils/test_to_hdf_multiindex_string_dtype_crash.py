
def test_to_hdf_multiindex_string_dtype_crash(temp_h5_path):
    # GH#63412
    index = MultiIndex.from_tuples([("a", "x"), ("b", "y")], names=["level1", "level2"])
    df = DataFrame({"value": [1, 2]}, index=index)
    df.to_hdf(temp_h5_path, key="test")
    result = read_hdf(temp_h5_path, key="test")
    tm.assert_frame_equal(df, result, check_dtype=False)

