
def test_parse_dates_dict_format_index(all_parsers):
    # GH#51240
    parser = all_parsers
    data = """a,b
2019-12-31,31-12-2019
2020-12-31,31-12-2020"""

    result = parser.read_csv(
        StringIO(data), date_format={"a": "%Y-%m-%d"}, parse_dates=True, index_col=0
    )
    expected = DataFrame(
        {
            "b": ["31-12-2019", "31-12-2020"],
        },
        index=Index([Timestamp("2019-12-31"), Timestamp("2020-12-31")], name="a"),
    )
    tm.assert_frame_equal(result, expected)

