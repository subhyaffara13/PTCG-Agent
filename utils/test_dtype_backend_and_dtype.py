
def test_dtype_backend_and_dtype(all_parsers):
    # GH#36712

    parser = all_parsers

    data = """a,b
1,2.5
,
"""
    result = parser.read_csv(
        StringIO(data), dtype_backend="numpy_nullable", dtype="float64"
    )
    expected = DataFrame({"a": [1.0, np.nan], "b": [2.5, np.nan]})
    tm.assert_frame_equal(result, expected)

