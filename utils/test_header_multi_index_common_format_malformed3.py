
def test_header_multi_index_common_format_malformed3(all_parsers):
    parser = all_parsers
    expected = DataFrame(
        np.array([[3, 4, 5, 6], [9, 10, 11, 12]], dtype="int64"),
        index=MultiIndex(levels=[[1, 7], [2, 8]], codes=[[0, 1], [0, 1]]),
        columns=MultiIndex(
            levels=[["a", "b", "c"], ["s", "t", "u", "v"]],
            codes=[[0, 1, 2, 2], [0, 1, 2, 3]],
            names=[None, "q"],
        ),
    )
    data = """,a,a,b,c,c
q,r,s,t,u,v
1,2,3,4,5,6
7,8,9,10,11,12"""

    result = parser.read_csv(StringIO(data), header=[0, 1], index_col=[0, 1])
    tm.assert_frame_equal(expected, result)

