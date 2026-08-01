
def test_to_html_float_format_no_fixed_width(value, float_format, expected, datapath):
    # GH 21625, GH 22270
    df = DataFrame({"x": [value]})
    expected = expected_html(datapath, expected)
    result = df.to_html(float_format=float_format)
    assert result == expected

