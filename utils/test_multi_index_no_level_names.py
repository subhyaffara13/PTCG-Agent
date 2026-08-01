
def test_multi_index_no_level_names(
    request, all_parsers, index_col, using_infer_string
):
    data = """index1,index2,A,B,C,D
foo,one,2,3,4,5
foo,two,7,8,9,10
foo,three,12,13,14,15
bar,one,12,13,14,15
bar,two,12,13,14,15
"""
    headless_data = "\n".join(data.split("\n")[1:])

    names = ["A", "B", "C", "D"]
    parser = all_parsers

    result = parser.read_csv(
        StringIO(headless_data), index_col=index_col, header=None, names=names
    )
    expected = parser.read_csv(StringIO(data), index_col=index_col)

    # No index names in headless data.
    expected.index.names = [None] * 2
    tm.assert_frame_equal(result, expected)

