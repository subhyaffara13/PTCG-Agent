
def test_header_multi_index_common_format1(all_parsers, kwargs):
    parser = all_parsers
    expected = DataFrame(
        [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]],
        index=["one", "two"],
        columns=MultiIndex.from_tuples(
            [("a", "q"), ("a", "r"), ("a", "s"), ("b", "t"), ("c", "u"), ("c", "v")]
        ),
    )
    data = """,a,a,a,b,c,c
,q,r,s,t,u,v
,,,,,,
one,1,2,3,4,5,6
two,7,8,9,10,11,12"""

    result = parser.read_csv(StringIO(data), index_col=0, **kwargs)
    tm.assert_frame_equal(result, expected)

