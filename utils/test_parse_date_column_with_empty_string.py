
def test_parse_date_column_with_empty_string(all_parsers):
    # see gh-6428
    parser = all_parsers
    data = "case,opdate\n7,10/18/2006\n7,10/18/2008\n621, "
    result = parser.read_csv(StringIO(data), parse_dates=["opdate"])

    expected_data = [[7, "10/18/2006"], [7, "10/18/2008"], [621, " "]]
    expected = DataFrame(expected_data, columns=["case", "opdate"])
    tm.assert_frame_equal(result, expected)

