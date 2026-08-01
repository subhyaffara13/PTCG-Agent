
def test_header_multiple_whitespaces(all_parsers):
    # GH#54931
    parser = all_parsers
    data = """aa    bb(1,1)   cc(1,1)
                0  2  3.5"""

    result = parser.read_csv(StringIO(data), sep=r"\s+")
    expected = DataFrame({"aa": [0], "bb(1,1)": 2, "cc(1,1)": 3.5})
    tm.assert_frame_equal(result, expected)

