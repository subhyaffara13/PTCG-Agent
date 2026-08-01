
def test_usecols_dtype(all_parsers):
    parser = all_parsers
    data = """
col1,col2,col3
a,1,x
b,2,y
"""
    result = parser.read_csv(
        StringIO(data),
        usecols=["col1", "col2"],
        dtype={"col1": "string", "col2": "uint8", "col3": "string"},
    )
    expected = DataFrame(
        {"col1": array(["a", "b"]), "col2": np.array([1, 2], dtype="uint8")}
    )
    tm.assert_frame_equal(result, expected)

