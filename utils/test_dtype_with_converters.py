
def test_dtype_with_converters(all_parsers):
    parser = all_parsers
    data = """a,b
1.1,2.2
1.2,2.3"""

    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data), dtype={"a": "i8"}, converters={"a": lambda x: str(x)}
            )
        return

    # Dtype spec ignored if converted specified.
    result = parser.read_csv_check_warnings(
        ParserWarning,
        "Both a converter and dtype were specified for column a "
        "- only the converter will be used.",
        StringIO(data),
        dtype={"a": "i8"},
        converters={"a": lambda x: str(x)},
    )
    expected = DataFrame({"a": ["1.1", "1.2"], "b": [2.2, 2.3]})
    tm.assert_frame_equal(result, expected)

