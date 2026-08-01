
def test_from_csv_with_mixed_offsets(all_parsers):
    parser = all_parsers
    data = "a\n2020-01-01T00:00:00+01:00\n2020-01-01T00:00:00+00:00"
    result = parser.read_csv(StringIO(data), parse_dates=["a"])["a"]
    expected = Series(
        [
            "2020-01-01T00:00:00+01:00",
            "2020-01-01T00:00:00+00:00",
        ],
        name="a",
        index=[0, 1],
    )
    tm.assert_series_equal(result, expected)

