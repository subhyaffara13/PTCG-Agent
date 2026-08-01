
def test_utf8_bom(all_parsers, data, kwargs, expected):
    # see gh-4793
    parser = all_parsers
    bom = "\ufeff"
    utf8 = "utf-8"

    def _encode_data_with_bom(_data):
        bom_data = (bom + _data).encode(utf8)
        return BytesIO(bom_data)

    if (
        parser.engine == "pyarrow"
        and data == "\n1"
        and kwargs.get("skip_blank_lines", True)
    ):
        # CSV parse error: Empty CSV file or block: cannot infer number of columns
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    result = parser.read_csv(_encode_data_with_bom(data), encoding=utf8, **kwargs)
    expected = DataFrame({"a": expected})
    tm.assert_frame_equal(result, expected)

