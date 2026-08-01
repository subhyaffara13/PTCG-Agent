
def test_to_html_multiindex(columns, justify, expected, datapath):
    df = DataFrame([list("abcd"), list("efgh")], columns=columns)
    result = df.to_html(justify=justify)
    expected = expected_html(datapath, expected)
    assert result == expected

