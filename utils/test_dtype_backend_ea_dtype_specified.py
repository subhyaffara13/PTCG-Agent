
def test_dtype_backend_ea_dtype_specified(all_parsers):
    # GH#491496
    data = """a,b
1,2
"""
    parser = all_parsers
    result = parser.read_csv(
        StringIO(data), dtype="Int64", dtype_backend="numpy_nullable"
    )
    expected = DataFrame({"a": [1], "b": 2}, dtype="Int64")
    tm.assert_frame_equal(result, expected)

