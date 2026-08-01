
def test_usecols_no_header_pyarrow(pyarrow_parser_only):
    parser = pyarrow_parser_only
    data = """
a,i,x
b,j,y
"""
    result = parser.read_csv(
        StringIO(data),
        header=None,
        usecols=[0, 1],
        dtype="string[pyarrow]",
        dtype_backend="pyarrow",
        engine="pyarrow",
    )
    expected = DataFrame([["a", "i"], ["b", "j"]], dtype="string[pyarrow]")
    tm.assert_frame_equal(result, expected)

