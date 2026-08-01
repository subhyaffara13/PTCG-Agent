
def test_encoding_temp_file(
    all_parsers, utf_value, encoding_fmt, pass_encoding, temp_file
):
    # see gh-24130
    parser = all_parsers
    encoding = encoding_fmt.format(utf_value)

    if parser.engine == "pyarrow" and pass_encoding is True and utf_value in [16, 32]:
        # FIXME: this is bad!
        pytest.skip("These cases freeze")

    expected = DataFrame({"foo": ["bar"]})

    with temp_file.open(mode="w+", encoding=encoding) as f:
        f.write("foo\nbar")
        f.seek(0)

        result = parser.read_csv(f, encoding=encoding if pass_encoding else None)
        tm.assert_frame_equal(result, expected)

