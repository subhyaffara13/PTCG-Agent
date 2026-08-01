
def test_parse_tz_aware(all_parsers):
    # See gh-1693
    parser = all_parsers
    data = "Date,x\n2012-06-13T01:39:00Z,0.5"

    result = parser.read_csv(StringIO(data), index_col=0, parse_dates=True)
    expected = DataFrame(
        {"x": [0.5]}, index=Index([Timestamp("2012-06-13 01:39:00+00:00")], name="Date")
    )
    if parser.engine == "pyarrow":
        expected.index = expected.index.as_unit("s")
    tm.assert_frame_equal(result, expected)
    assert result.index.tz is timezone.utc

