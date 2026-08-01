
def test_usecols_index_col_false(all_parsers, data):
    # see gh-9082
    parser = all_parsers
    usecols = ["a", "c", "d"]
    expected = DataFrame({"a": [1, 5], "c": [3, 7], "d": [4, 8]})

    result = parser.read_csv(StringIO(data), usecols=usecols, index_col=False)
    tm.assert_frame_equal(result, expected)

