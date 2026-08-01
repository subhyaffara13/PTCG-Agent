
def test_ignore_display_max_colwidth(method, expected, max_colwidth):
    # see gh-17004
    df = DataFrame([lorem_ipsum])
    with option_context("display.max_colwidth", max_colwidth):
        result = getattr(df, method)()
    expected = expected(max_colwidth)
    assert expected in result

