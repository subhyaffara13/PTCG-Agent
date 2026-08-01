
def test_header_multi_index_common_format3(all_parsers, kwargs):
    parser = all_parsers
    expected = DataFrame(
        [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]],
        index=["one", "two"],
        columns=MultiIndex.from_tuples(
            [("a", "q"), ("a", "r"), ("a", "s"), ("b", "t"), ("c", "u"), ("c", "v")]
        ),
    )
    expected = expected.reset_index(drop=True)
    data = """a,a,a,b,c,c
q,r,s,t,u,v
1,2,3,4,5,6
7,8,9,10,11,12"""

    result = parser.read_csv(StringIO(data), index_col=None, **kwargs)
    tm.assert_frame_equal(result, expected)

