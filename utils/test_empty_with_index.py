
def test_empty_with_index(all_parsers):
    # see gh-10184
    data = "x,y"
    parser = all_parsers
    result = parser.read_csv(StringIO(data), index_col=0)

    expected = DataFrame(columns=["y"], index=Index([], name="x"))
    tm.assert_frame_equal(result, expected)

