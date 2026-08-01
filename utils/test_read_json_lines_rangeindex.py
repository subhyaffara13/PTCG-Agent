
def test_read_json_lines_rangeindex():
    # GH 57429
    data = """
{"a": 1, "b": 2}
{"a": 3, "b": 4}
"""
    result = read_json(StringIO(data), lines=True).index
    expected = RangeIndex(2)
    tm.assert_index_equal(result, expected, exact=True)

