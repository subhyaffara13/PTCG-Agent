
def test_parse_dates_and_string_dtype(all_parsers):
    # GH#34066
    parser = all_parsers
    data = """a,b
1,2019-12-31
"""
    result = parser.read_csv(StringIO(data), dtype="string", parse_dates=["b"])
    expected = DataFrame({"a": ["1"], "b": [Timestamp("2019-12-31")]})
    expected["a"] = expected["a"].astype("string")
    tm.assert_frame_equal(result, expected)

