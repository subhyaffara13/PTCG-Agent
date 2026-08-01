
def test_usecols_index_col_middle(all_parsers):
    # GH#9098
    parser = all_parsers
    data = """a,b,c,d
1,2,3,4
"""
    result = parser.read_csv(StringIO(data), usecols=["b", "c", "d"], index_col="c")
    expected = DataFrame({"b": [2], "d": [4]}, index=Index([3], name="c"))
    tm.assert_frame_equal(result, expected)

