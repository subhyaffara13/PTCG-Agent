
def test_first_row_bom_unquoted(all_parsers):
    # see gh-36343
    parser = all_parsers
    data = """\ufeffHead1\tHead2\tHead3"""

    result = parser.read_csv(StringIO(data), delimiter="\t")
    expected = DataFrame(columns=["Head1", "Head2", "Head3"])
    tm.assert_frame_equal(result, expected)

