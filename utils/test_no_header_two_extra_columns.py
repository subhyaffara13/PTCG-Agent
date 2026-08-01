
def test_no_header_two_extra_columns(all_parsers):
    # GH 26218
    column_names = ["one", "two", "three"]
    ref = DataFrame([["foo", "bar", "baz"]], columns=column_names)
    stream = StringIO("foo,bar,baz,bam,blah")
    parser = all_parsers
    df = parser.read_csv_check_warnings(
        ParserWarning,
        "Length of header or names does not match length of data. "
        "This leads to a loss of data with index_col=False.",
        stream,
        header=None,
        names=column_names,
        index_col=False,
    )
    tm.assert_frame_equal(df, ref)

