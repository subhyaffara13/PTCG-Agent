
def test_to_html_border(option, result, expected):
    df = DataFrame({"A": [1, 2]})
    if option is None:
        result = result(df)
    else:
        with option_context("display.html.border", option):
            result = result(df)
    expected = f'border="{expected}"'
    assert expected in result

