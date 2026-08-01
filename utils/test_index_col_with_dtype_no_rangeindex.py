
def test_index_col_with_dtype_no_rangeindex(all_parsers):
    data = StringIO("345.5,519.5,0\n519.5,726.5,1")
    result = all_parsers.read_csv(
        data,
        header=None,
        names=["start", "stop", "bin_id"],
        dtype={"start": np.float32, "stop": np.float32, "bin_id": np.uint32},
        index_col="bin_id",
    ).index
    expected = pd.Index([0, 1], dtype=np.uint32, name="bin_id")
    tm.assert_index_equal(result, expected)

