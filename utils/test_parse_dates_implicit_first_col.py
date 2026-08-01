
def test_parse_dates_implicit_first_col(all_parsers):
    data = """A,B,C
20090101,a,1,2
20090102,b,3,4
20090103,c,4,5
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data), parse_dates=True)

    expected = parser.read_csv(StringIO(data), index_col=0, parse_dates=True)
    tm.assert_frame_equal(result, expected)

