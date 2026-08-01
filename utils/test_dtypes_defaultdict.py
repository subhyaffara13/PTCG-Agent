
def test_dtypes_defaultdict(all_parsers, default):
    # GH#41574
    data = """a,b
1,2
"""
    dtype = defaultdict(lambda: default, a="int64")
    parser = all_parsers
    result = parser.read_csv(StringIO(data), dtype=dtype)
    expected = DataFrame({"a": [1], "b": 2.0})
    tm.assert_frame_equal(result, expected)

