
def test_parse_dates_empty_string(all_parsers):
    # see gh-2263
    parser = all_parsers
    data = "Date,test\n2012-01-01,1\n,2"
    result = parser.read_csv(StringIO(data), parse_dates=["Date"], na_filter=False)

    expected = DataFrame(
        [[datetime(2012, 1, 1), 1], [pd.NaT, 2]], columns=["Date", "test"]
    )
    tm.assert_frame_equal(result, expected)

