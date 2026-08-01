
def test_numeric_dtype(all_parsers, any_real_numpy_dtype):
    data = "0\n1"
    parser = all_parsers
    expected = DataFrame([0, 1], dtype=any_real_numpy_dtype)

    result = parser.read_csv(StringIO(data), header=None, dtype=any_real_numpy_dtype)
    tm.assert_frame_equal(expected, result, check_column_type=False)

