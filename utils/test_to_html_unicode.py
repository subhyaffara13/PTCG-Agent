
def test_to_html_unicode(df_data, expected, datapath):
    df = DataFrame(df_data)
    expected = expected_html(datapath, expected)
    result = df.to_html()
    assert result == expected

