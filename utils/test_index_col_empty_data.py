
def test_index_col_empty_data(all_parsers, index_col, kwargs):
    data = "x,y,z"
    parser = all_parsers
    result = parser.read_csv(StringIO(data), index_col=index_col)

    expected = DataFrame(**kwargs)
    tm.assert_frame_equal(result, expected)

