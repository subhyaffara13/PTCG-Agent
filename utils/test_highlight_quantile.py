
def test_highlight_quantile(styler, kwargs):
    expected = {
        (2, 0): [("background-color", "yellow")],
        (2, 1): [("background-color", "yellow")],
    }
    result = styler.highlight_quantile(**kwargs)._compute().ctx
    assert result == expected

