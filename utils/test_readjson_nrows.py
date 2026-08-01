
def test_readjson_nrows(nrows, engine):
    # GH 33916
    # Test reading line-format JSON to Series with nrows param
    jsonl = """{"a": 1, "b": 2}
        {"a": 3, "b": 4}
        {"a": 5, "b": 6}
        {"a": 7, "b": 8}"""
    result = read_json(StringIO(jsonl), lines=True, nrows=nrows)
    expected = DataFrame({"a": [1, 3, 5, 7], "b": [2, 4, 6, 8]}).iloc[:nrows]
    tm.assert_frame_equal(result, expected)

