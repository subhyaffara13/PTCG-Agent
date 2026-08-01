
def test_parse_dates_arrow_engine(all_parsers):
    # GH#53295
    parser = all_parsers
    data = """a,b
2000-01-01 00:00:00,1
2000-01-01 00:00:01,1"""

    result = parser.read_csv(StringIO(data), parse_dates=["a"])
    expected = DataFrame(
        {
            "a": [
                Timestamp("2000-01-01 00:00:00"),
                Timestamp("2000-01-01 00:00:01"),
            ],
            "b": 1,
        }
    )
    if parser.engine == "pyarrow":
        expected["a"] = expected["a"].astype("M8[s]")
    tm.assert_frame_equal(result, expected)

