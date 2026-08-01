
def test_date_parser_and_names(all_parsers):
    # GH#33699
    parser = all_parsers
    data = StringIO("""x,y\n1,2""")
    warn = UserWarning
    if parser.engine == "pyarrow":
        # Pandas4Warning for passing a Manager object
        warn = (UserWarning, Pandas4Warning)
    result = parser.read_csv_check_warnings(
        warn,
        "Could not infer format",
        data,
        parse_dates=["B"],
        names=["B"],
    )
    expected = DataFrame({"B": ["y", "2"]}, index=["x", "1"])
    tm.assert_frame_equal(result, expected)

