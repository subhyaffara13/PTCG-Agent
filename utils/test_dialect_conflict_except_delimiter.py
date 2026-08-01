
def test_dialect_conflict_except_delimiter(all_parsers, custom_dialect, arg, value):
    # see gh-23761.
    dialect_name, dialect_kwargs = custom_dialect
    parser = all_parsers

    expected = DataFrame({"a": [1], "b": [2]})
    data = "a:b\n1:2"

    warning_klass = None
    kwds = {}

    # arg=None tests when we pass in the dialect without any other arguments.
    if arg is not None:
        if value == "dialect":  # No conflict --> no warning.
            kwds[arg] = dialect_kwargs[arg]
        elif value == "default":  # Default --> no warning.
            from pandas.io.parsers.base_parser import parser_defaults

            kwds[arg] = parser_defaults[arg]
        else:  # Non-default + conflict with dialect --> warning.
            warning_klass = ParserWarning
            kwds[arg] = "blah"

    with tm.with_csv_dialect(dialect_name, **dialect_kwargs):
        if parser.engine == "pyarrow":
            msg = "The 'dialect' option is not supported with the 'pyarrow' engine"
            with pytest.raises(ValueError, match=msg):
                parser.read_csv_check_warnings(
                    # No warning bc we raise
                    None,
                    "Conflicting values for",
                    StringIO(data),
                    dialect=dialect_name,
                    **kwds,
                )
            return
        result = parser.read_csv_check_warnings(
            warning_klass,
            "Conflicting values for",
            StringIO(data),
            dialect=dialect_name,
            **kwds,
        )
        tm.assert_frame_equal(result, expected)

