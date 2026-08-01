
def test_empty_na_values_no_default_with_index(all_parsers):
    # see gh-15835
    data = "a,1\nb,2"
    parser = all_parsers
    expected = DataFrame({"1": [2]}, index=Index(["b"], name="a"))

    result = parser.read_csv(StringIO(data), index_col=0, keep_default_na=False)
    tm.assert_frame_equal(result, expected)

