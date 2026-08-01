
def test_parse_dates_column_list(all_parsers, parse_dates):
    data = "a,b,c\n01/01/2010,1,15/02/2010"
    parser = all_parsers

    expected = DataFrame(
        {"a": [datetime(2010, 1, 1)], "b": [1], "c": [datetime(2010, 2, 15)]}
    )
    expected["a"] = expected["a"].astype("M8[us]")
    expected["c"] = expected["c"].astype("M8[us]")
    expected = expected.set_index(["a", "b"])

    result = parser.read_csv(
        StringIO(data), index_col=[0, 1], parse_dates=parse_dates, dayfirst=True
    )
    tm.assert_frame_equal(result, expected)

