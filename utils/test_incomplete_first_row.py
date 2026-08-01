
def test_incomplete_first_row(all_parsers, usecols):
    # see gh-6710
    data = "1,2\n1,2,3"
    parser = all_parsers
    names = ["a", "b", "c"]
    expected = DataFrame({"a": [1, 1], "c": [np.nan, 3]})

    result = parser.read_csv(StringIO(data), names=names, usecols=usecols)
    tm.assert_frame_equal(result, expected)

