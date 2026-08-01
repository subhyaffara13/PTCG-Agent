
def test_parse_dates_dict_format(all_parsers):
    # GH#51240
    parser = all_parsers
    data = """a,b
2019-12-31,31-12-2019
2020-12-31,31-12-2020"""

    result = parser.read_csv(
        StringIO(data),
        date_format={"a": "%Y-%m-%d", "b": "%d-%m-%Y"},
        parse_dates=["a", "b"],
    )
    expected = DataFrame(
        {
            "a": [Timestamp("2019-12-31"), Timestamp("2020-12-31")],
            "b": [Timestamp("2019-12-31"), Timestamp("2020-12-31")],
        },
        dtype="M8[us]",
    )
    tm.assert_frame_equal(result, expected)

