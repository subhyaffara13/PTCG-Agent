
def test_custom_lineterminator(c_parser_only):
    parser = c_parser_only
    data = "a,b,c~1,2,3~4,5,6"

    result = parser.read_csv(StringIO(data), lineterminator="~")
    expected = parser.read_csv(StringIO(data.replace("~", "\n")))

    tm.assert_frame_equal(result, expected)

