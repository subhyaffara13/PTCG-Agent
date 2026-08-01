
def test_inf_parsing(all_parsers, na_filter):
    parser = all_parsers
    data = """\
,A
a,inf
b,-inf
c,+Inf
d,-Inf
e,INF
f,-INF
g,+INf
h,-INf
i,inF
j,-inF"""
    expected = DataFrame(
        {"A": [float("inf"), float("-inf")] * 5},
        index=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )
    result = parser.read_csv(StringIO(data), index_col=0, na_filter=na_filter)
    tm.assert_frame_equal(result, expected)

