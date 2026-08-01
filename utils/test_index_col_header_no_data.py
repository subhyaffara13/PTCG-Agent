
def test_index_col_header_no_data(all_parsers):
    # GH#38292
    parser = all_parsers
    result = parser.read_csv(StringIO("a0,a1,a2\n"), header=[0], index_col=0)
    expected = DataFrame(
        [],
        columns=["a1", "a2"],
        index=Index([], name="a0"),
    )
    tm.assert_frame_equal(result, expected)

