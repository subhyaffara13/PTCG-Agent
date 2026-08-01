
def test_to_html_formatters(df, formatters, expected, datapath):
    expected = expected_html(datapath, expected)
    result = df.to_html(formatters=formatters)
    assert result == expected

