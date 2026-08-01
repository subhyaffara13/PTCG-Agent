
def test_dialect_conflict_delimiter(all_parsers, custom_dialect, kwargs, warning_klass):
    # see gh-23761.
    dialect_name, dialect_kwargs = custom_dialect
    parser = all_parsers

    expected = DataFrame({"a": [1], "b": [2]})
    data = "a:b\n1:2"

    with tm.with_csv_dialect(dialect_name, **dialect_kwargs):
        if parser.engine == "pyarrow":
            msg = "The 'dialect' option is not supported with the 'pyarrow' engine"
            with pytest.raises(ValueError, match=msg):
                parser.read_csv_check_warnings(
                    # no warning bc we raise
                    None,
                    "Conflicting values for 'delimiter'",
                    StringIO(data),
                    dialect=dialect_name,
                    **kwargs,
                )
            return
        result = parser.read_csv_check_warnings(
            warning_klass,
            "Conflicting values for 'delimiter'",
            StringIO(data),
            dialect=dialect_name,
            **kwargs,
        )
        tm.assert_frame_equal(result, expected)

