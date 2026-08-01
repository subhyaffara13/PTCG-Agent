
def test_comment_header(all_parsers):
    parser = all_parsers
    data = """# empty
# second empty line
1,2,3
A,B,C
1,2.,4.
5.,NaN,10.0
"""
    # Header should begin at the second non-comment line.
    expected = DataFrame(
        [[1.0, 2.0, 4.0], [5.0, np.nan, 10.0]], columns=["A", "B", "C"]
    )
    if parser.engine == "pyarrow":
        msg = "The 'comment' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), comment="#", header=1)
        return
    result = parser.read_csv(StringIO(data), comment="#", header=1)
    tm.assert_frame_equal(result, expected)

