
def test_on_bad_lines_callable_warns_and_truncates_with_index_col(
    python_parser_only, index_col
):
    # GH#61837
    parser = python_parser_only
    data = "id,field_1,field_2\n101,A,B\n102,C,D,E\n103,F,G\n"

    def fixer(bad_line):
        return [*list(bad_line), "EXTRA1", "EXTRA2"]

    result = parser.read_csv_check_warnings(
        ParserWarning,
        "from bad_lines callable",
        StringIO(data),
        on_bad_lines=fixer,
        index_col=index_col,
    )

    if index_col is None:
        expected = DataFrame(
            {
                "id": [101, 102, 103],
                "field_1": ["A", "C", "F"],
                "field_2": ["B", "D", "G"],
            }
        )
    else:
        expected = DataFrame(
            {"field_1": ["A", "C", "F"], "field_2": ["B", "D", "G"]},
            index=Index([101, 102, 103], name="id"),
        )

    tm.assert_frame_equal(result, expected)

