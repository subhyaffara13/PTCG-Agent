
def test_decompression_regex_sep(
    temp_file, python_parser_only, csv1, compression, klass
):
    # see gh-6607
    parser = python_parser_only

    with open(csv1, "rb") as f:
        data = f.read()

    data = data.replace(b",", b"::")
    expected = parser.read_csv(csv1)

    module = pytest.importorskip(compression)
    klass = getattr(module, klass)

    with klass(temp_file, mode="wb") as tmp:
        tmp.write(data)

    result = parser.read_csv(temp_file, sep="::", compression=compression)
    tm.assert_frame_equal(result, expected)

