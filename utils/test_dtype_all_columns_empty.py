
def test_dtype_all_columns_empty(all_parsers):
    # see gh-12048
    parser = all_parsers
    result = parser.read_csv(StringIO("A,B"), dtype=str)

    expected = DataFrame({"A": [], "B": []}, dtype=str)
    tm.assert_frame_equal(result, expected)

