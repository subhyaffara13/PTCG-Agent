
def test_integer_precision(all_parsers):
    # Gh 7072
    s = """1,1;0;0;0;1;1;3844;3844;3844;1;1;1;1;1;1;0;0;1;1;0;0,,,4321583677327450765
5,1;0;0;0;1;1;843;843;843;1;1;1;1;1;1;0;0;1;1;0;0,64.0,;,4321113141090630389"""
    parser = all_parsers
    result = parser.read_csv(StringIO(s), header=None)[4]
    expected = Series([4321583677327450765, 4321113141090630389], name=4)
    tm.assert_series_equal(result, expected)

